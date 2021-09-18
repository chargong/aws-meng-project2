import os
import boto3
from bottle import route, request, run
import logging


INPUT_BUCKET_NAME = "asu-project2-input-ghh"
QUEUE_NAME = "asu-project2-queue-ghh"
REGION = "ap-northeast-2"
AK = "mockak"
SK = "mocksk"


@route('/')
def root():
    return "ok"


@route('/upload', method='POST')
def do_upload():
    upload = request.files.get('myfile')
    name, ext = os.path.splitext(upload.filename)
    if ext not in ('.JPEG', '.jpeg'):
        return "File extension not allowed."
    file_tmp_path = "/tmp/%s" % upload.filename
    if not os.path.exists(file_tmp_path):
        upload.save(file_tmp_path)
    # upload file to s3
    s3_client = boto3.client('s3', region_name=REGION, aws_access_key_id=AK,
                             aws_secret_access_key=SK)
    s3_client.upload_file(file_tmp_path, INPUT_BUCKET_NAME, upload.filename)
    s3_path = upload.filename
    # send message to sqs
    send_sqs(s3_path)

    # echo
    return "File successfully uploaded %s" % s3_path


def send_sqs(s3_path):
    sqs = boto3.resource('sqs', region_name=REGION, aws_access_key_id=AK,
                         aws_secret_access_key=SK)
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    response = queue.send_message(MessageBody=s3_path)
    logging.info(response)


if __name__ == '__main__':
    run(host='0.0.0.0', port=8080, server='gunicorn', workers=4)
