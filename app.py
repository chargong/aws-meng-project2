import logging

import boto3
import time

import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import json
import sys
import numpy as np


INPUT_BUCKET_NAME = "asu-project2-input-ghh"
OUTPUT_BUCKET_NAME = "asu-project2-output-ghh"
QUEUE_URL = 'https://sqs.ap-northeast-2.amaonaws.com/278365270497/asu-project2-queue-ghh'
QUEUE_NAME = 'asu-project2-queue-ghh'
REGION = "ap-northeast-2"
AK = "mockak"
SK = "mocksk"


def classify(path):
    img = Image.open(path)
    model = models.resnet18(pretrained=True)

    model.eval()
    img_tensor = transforms.ToTensor()(img).unsqueeze_(0)
    outputs = model(img_tensor)
    _, predicted = torch.max(outputs.data, 1)

    with open('./imagenet-labels.json') as f:
        labels = json.load(f)
    result = labels[np.array(predicted)[0]]
    return result


def execute_via_queue():
    while True:
        sqs = boto3.resource("sqs",
                             region_name=REGION, aws_access_key_id=AK,
                             aws_secret_access_key=SK)
        s3_client = boto3.client('s3', region_name=REGION, aws_access_key_id=AK,
                                 aws_secret_access_key=SK)
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
        msg_list = queue.receive_messages(
            AttributeNames=['All'],
            MessageAttributeNames=['All'],
            MaxNumberOfMessages=3,
            VisibilityTimeout=600,
            WaitTimeSeconds=4)
        for message in msg_list:
            file_name = message.body
            logging.info(file_name)
            try:
                s3_client.download_file(INPUT_BUCKET_NAME, file_name, "/tmp/" + file_name)
                identity = classify("/tmp/" + file_name)
                logging.info(identity)

                s3_client.upload_file(OUTPUT_BUCKET_NAME, identity, "/tmp/" + file_name)
                message.delete()
            except Exception as e:
                logging.exception(e)
                logging.error("download failed %s" % file_name)

        if len(msg_list) == 0:
            logging.info("no work, sleep a while")
            time.sleep(3)


if __name__ == '__main__':
    execute_via_queue()
