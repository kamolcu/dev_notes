# pip install paramiko
import paramiko
import subprocess
import sys
import json

def ips_from_tag_name(name):
    command_template = 'aws ec2 describe-instances --filters "Name=tag:Name,Values=%s"'
    target_command = command_template % name
    p = subprocess.Popen(target_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (ret, err) = p.communicate()
    if err is not None and len(err.strip()) > 0:
        sys.exit(err)
    jj = json.loads(ret)
    ec_two_list = jj['Reservations']
    ec_two_s = []
    for ec_two_inst in ec_two_list:
        ec_two_s.append(ec_two_inst)
    ips = []
    for ec_two in ec_two_s:
        ips.append(ec_two['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddresses'][0]['PrivateIpAddress'])
    return ips


def print_version(host, private_key, command, environment_string):
    client.connect(host, username='root', pkey=private_key)
    stdin, stdout, stderr = client.exec_command(command)
    print '===%s-%s-version.txt===:' % (environment_string, host)
    for line in stdout:
        print line.strip('\n')
    print ''
    client.close()

# Name awsa-mpds-apibe,awsa-mmch-apibe
alpha_apibe_names = ['awsa-mpds-apibe', 'awsa-mmch-apibe']
# awsa-mpds-webfe
alpha_cmsfe_names = ['awsa-mpds-webfe']
# Name awss-mpds-apibe,awss-mmch-apibe
staging_apibe_names = ['awss-mpds-apibe', 'awss-mmch-apibe']
# awss-mpds-webfe
staging_cmsfe_names = ['awss-mpds-webfe']

version_read_command = 'cat /opt/tomcat-latest/webapps/version.txt'
frontend_version_read_command = 'cat /data/projects/pds-backoffice/version.txt'
alpha_host_key = paramiko.RSAKey.from_private_key_file('./ITM-ALPHA.pem')
staging_host_key = paramiko.RSAKey.from_private_key_file('./ITM-STAGING.pem')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Main
print ''
for name in alpha_apibe_names:
    ips = ips_from_tag_name(name)
    for ip in ips:
        print_version(ip, alpha_host_key, version_read_command, 'Alpha')

for name in alpha_cmsfe_names:
    ips = ips_from_tag_name(name)
    for ip in ips:
        print_version(ip, alpha_host_key, frontend_version_read_command, 'Alpha-Backoffice')

for name in staging_apibe_names:
    ips = ips_from_tag_name(name)
    for ip in ips:
        print_version(ip, staging_host_key, version_read_command, 'Staging')

for name in staging_cmsfe_names:
    ips = ips_from_tag_name(name)
    for ip in ips:
        print_version(ip, staging_host_key, frontend_version_read_command, 'Staging-Backoffice')

# for ip in alpha_frontend_ips:
#     print_version(ip, alpha_host_key, frontend_version_read_command, 'Alpha-Backoffice')

# for ip in staging_ips:
#     print_version(ip, staging_host_key, version_read_command, 'Staging')

# for ip in staging_frontend_ips:
#     print_version(ip, staging_host_key, frontend_version_read_command, 'Staging-Backoffice')
