# pip install paramiko
import paramiko

def print_version(host, private_key, command, environment_string):
    client.connect(host, username='root', pkey=private_key)
    stdin, stdout, stderr = client.exec_command(command)
    print '===%s-%s-version.txt===:' % (environment_string, host)
    for line in stdout:
        print line.strip('\n')
    print ''
    client.close()

# Name awsa-mpds-apibe,awsa-mmch-apibe
alpha_ips = ['10.229.13.56', '10.229.13.23', '10.229.13.61']
# awsa-mpds-webfe
alpha_frontend_ips = ['10.229.12.99']
# Name awss-mpds-apibe,awss-mmch-apibe
staging_ips = ['10.229.1.148', '10.229.1.33', '10.229.1.31', '10.229.1.165']
# awss-mpds-webfe
staging_frontend_ips = ['10.229.0.55', '10.229.0.212']

version_read_command = 'cat /opt/tomcat-latest/webapps/version.txt'
frontend_version_read_command = 'cat /data/projects/pds-backoffice/version.txt'
alpha_host_key = paramiko.RSAKey.from_private_key_file('./ITM-ALPHA.pem')
staging_host_key = paramiko.RSAKey.from_private_key_file('./ITM-STAGING.pem')
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Main
print ''
for ip in alpha_ips:
    print_version(ip, alpha_host_key, version_read_command, 'Alpha')

for ip in alpha_frontend_ips:
    print_version(ip, alpha_host_key, frontend_version_read_command, 'Alpha-Backoffice')

for ip in staging_ips:
    print_version(ip, staging_host_key, version_read_command, 'Staging')

for ip in staging_frontend_ips:
    print_version(ip, staging_host_key, frontend_version_read_command, 'Staging-Backoffice')
