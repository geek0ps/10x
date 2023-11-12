# Python

## Directory Cleanup

```python

import os
import shutil
import time

def cleanup_dir(path, days_old):
    current_time = time.time()
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        creation_time = os.path.getctime(file_path)
        if (current_time - creation_time) // (24 * 3600) >= days_old:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

cleanup_dir('/path/to/dir', 30)  # Clean files older than 30 days


```

## Log Parser

```python

def parse_log(file_path, keyword):
    with open(file_path, 'r') as file:
        for line in file:
            if keyword in line:
                print(line)

parse_log('/path/to/logfile.log', 'ERROR')


```


## Backup Script

```python

import shutil

def backup(src, dest):
    shutil.copytree(src, dest)

backup('/path/to/source', '/path/to/backup')


```


## System Health Check

```python
import psutil

def system_health():
    print("CPU usage:", psutil.cpu_percent(interval=1))
    print("Memory usage:", psutil.virtual_memory().percent)
    print("Disk usage:", psutil.disk_usage('/').percent)

system_health()


```



## Python Environment Setup

```python

import subprocess

def setup_environment(packages):
    for package in packages:
        subprocess.run(["pip", "install", package])

setup_environment(['flask', 'requests'])

```

## Service Monitoring

```python

import subprocess

def check_service(service_name):
    status = subprocess.run(["systemctl", "status", service_name], capture_output=True)
    return 'active' in str(status.stdout)

print(check_service('nginx'))


```


## Network Scanner

```python

import subprocess

def scan_network(ip):
    subprocess.run(["nmap", "-sP", ip])

scan_network('192.168.1.0/24')


```


## User Management

```python

import subprocess

def manage_user(action, username):
    subprocess.run(["user" + action, username])

manage_user('add', 'newuser')


```


## SSL CERT Checker

```python

import ssl
import socket
from datetime import datetime

def check_ssl_expiry(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
            return expiry

print(check_ssl_expiry('www.example.com'))

```


## Security Audit

```python

import subprocess

def run_security_scan(scan_tool, target):
    subprocess.run([scan_tool, target])

run_security_scan('nmap', '192.168.1.1')


```

## Automated Deployment

```python

import paramiko

def ssh_command(ssh_client, command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print(stdout.read().decode())
    print(stderr.read().decode())

def deploy_code_via_ssh(host, port, username, password, local_path, remote_path, user_script):
    # Establishing an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, port=port, username=username, password=password)

    # SCP Client to transfer files
    scp_client = paramiko.SCPClient(ssh_client.get_transport())

    # Transfer files to remote
    scp_client.put(local_path, remote_path)

    # Execute user script
    ssh_command(ssh_client, f"bash {user_script}")

    # Close connections
    scp_client.close()
    ssh_client.close()

# Example usage
deploy_code_via_ssh(
    host='192.168.1.100',
    port=22,
    username='your_username',
    password='your_password',
    local_path='/path/to/local/code',
    remote_path='/path/to/remote/destination',
    user_script='/path/to/remote/user_script.sh'
)

```