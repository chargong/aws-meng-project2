#  connect ssh ,send file and return a result.
import os
import paramiko
from paramiko import SSHClient, AutoAddPolicy

from rich import print, pretty, inspect
pretty.install()

client = SSHClient()
key = os.path.expanduser('~/.aws/cse546.pem')
key = paramiko.RSAKey.from_private_key_file(key)

# client.load_host_keys('~/.ssh/known_hosts')
# client.load_system_host_keys()

client.set_missing_host_key_policy(AutoAddPolicy)
ip_address ='15.164.250.88'
# client.connect('54.180.89.71',username='ubuntu')
client.connect(ip_address, username='ubuntu', pkey=key)

sftp_client = client.open_sftp()
sftp_client.chdir("/home/ubuntu/classifier/")
# stdin, stdout, stderr = client.exec_command('cd /home/ubuntu/classifier/')
# sftp_client.chdir("/home/ubuntu/classifier/")

sftp_client.put( os.path.expanduser('imagenet-100/test_0.JPEG'),'/upload_image/test_0.JPEG')

stdin, stdout, stderr = client.exec_command('python3 image_classification.py /upload_image/test_0.JPEG')
print(type(stdin))
print(type(stdout))
print(type(stderr))

if stdout.channel.recv_exit_status() == 0:

    print(stdout.read().decode("utf8"))
else:
    print(stderr.read().decode("utf8"))

print(f'Return code:{stdout.channel.recv_exit_status()}')

client.close()
