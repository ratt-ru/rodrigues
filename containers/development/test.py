#!/usr/bin/env python

from docker.client import Client
from docker.utils import kwargs_from_env
import os

HERE = os.path.dirname(os.path.abspath(__file__))

image_name = 'simulation/development'

kwargs = kwargs_from_env()
kwargs['tls'].assert_hostname = False
client = Client(**kwargs)

cid = client.create_container(image_name, '/run.sh')
client.start(cid, binds={HERE: {'bind': '/config', 'ro': True}})

print(client.wait(cid))
print(client.logs(cid))
