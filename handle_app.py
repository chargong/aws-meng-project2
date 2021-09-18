import boto3
from boto3.resources.model import Parameter

region ="ap-northeast-2"

ec2 = boto3.resource('ec2', region_name=region)

instance_running = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
instance_ids = [instance.id for instance in instance_running]

print(instance_ids)


def run_remote_cmd(instance_Id,region='ap-northeast-2'):

    ssm_client = boto3.client('ssm',region_name = region)
    response = ssm_client.send_command(InstanceIds =[instance_Id],DocumentName="AWS-RunShellScript",Parameters={'command':['sudo systemctl status amazon-ssm-agent']},)
    command_id =response['Command']['CommandId']
    output = ssm_client.get_command_invocation(CommandId= command_id,InstanceId=instance_Id)
    while output['Status'] == 'InProgress':
        output = ssm_client.get_command_invocation(CommandId= command_id,InstanceId=instance_Id)
    print(output['StandardOutputContent'])

def get_public_ip(instance_id): # get public address. can return a list of ips
    ec2 = boto3.client("ec2",region_name='ap-northeast-2')
    reservations =ec2.describe_instances(InstanceIds=[instance_id]).get("Reservations")
    ip=[]
    for reservation in reservations:
        for instance in reservation["Instances"]:
             ip.append(instance.get('PublicIpAddress'))
             
    return ip
    


p = get_public_ip(instance_ids[0])
print(p)

