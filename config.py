# this reads config from environment.. if you want, you can just place your
# config here (see config.py.example), but i don't reccomend you to publish it
# then :)

import os

server = os.environ['CA_REDIS_SERVER']
port = int(os.environ['CA_REDIS_PORT'])
password = os.environ['CA_REDIS_PASSWORD']
