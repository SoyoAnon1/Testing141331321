import getpass
import os
import subprocess
import requests
import base64
from re import sub

def Connect(password):
    subprocess.call("apt-get install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen > /dev/null", shell=True)
    subprocess.call(f'echo root:{password} | chpasswd',shell=True)
    subprocess.call('mkdir -p /var/run/sshd', shell=True)
    subprocess.call('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config', shell=True)
    subprocess.call('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config', shell=True)
    print("username: root")
    print("password: ", password)
    get_ipython().system_raw(base64.b64decode("c2VydmljZSBzc2ggc3RhcnQ=").decode())
    subprocess.call('wget -q -c -nc https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz',shell=True)
    subprocess.call('tar -xvzf ngrok-v3-stable-linux-amd64.tgz', shell=True)
    print("Get your authtoken from https://dashboard.ngrok.com/auth")
    authtoken = getpass.getpass()
    get_ipython().system_raw('./ngrok config add-authtoken $authtoken && ./ngrok tcp 22 &')

def VSConfig(str):
    print("Host VSConfig")
    print(f"\tHostName {str[6:20]}")
    print("\tUser root")
    print(f"\tPort {str[21:26]}")

def GetSSH():
    tun = requests.get('http://localhost:4040/api/tunnels')
    url = tun.json()['tunnels'][0]['public_url']
    str_ssh = sub("tcp://", "", url)
    str_ssh = sub(":", " -p ", str_ssh)
    str_ssh = "ssh root@" + str_ssh
    print("Tunnel URL: ")
    print(url)
    print("SSH Command: ")
    print(str_ssh)
    

def Kill():
    os.system("kill $(ps aux | grep './ngrok' | awk '{print $2}')")
