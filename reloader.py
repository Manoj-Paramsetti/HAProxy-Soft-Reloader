#!/bin/python3

import os
import time
from hashlib import sha256
import subprocess

file_content = str(open('/etc/haproxy/haproxy.cfg').readlines())
intial_hash = sha256(file_content.encode('UTF-8')).hexdigest()

old_hash = intial_hash

def initial_run():
    os.system('touch /var/run/haproxy.pid')

old_process_id = None
def soft_reload():
    global old_process_id
    print("[HAProxy Reloader]: New HAProxy Creating...")
    with open('/var/run/haproxy.pid', 'r') as pid_file:
        pid = pid_file.read().strip()
    command = [
        '/usr/local/sbin/haproxy',
        '-f', '/etc/haproxy/haproxy.cfg',
        '-p', '/var/run/haproxy.pid',
        '-sf'
    ]

    if (pid!= ""):
        command.append(pid) 

    master = subprocess.Popen(command, shell=False)
    old_process_id = master.pid

initial_run()
soft_reload()

while(True):
    file_content = str(open('/etc/haproxy/haproxy.cfg').readlines())
    new_hash = sha256(file_content.encode('UTF-8')).hexdigest()
    if(old_hash != new_hash):
        print("[HAProxy Reloader]: Configuration Changed!")
        soft_reload()
    old_hash = new_hash
    time.sleep(5)