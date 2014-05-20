# this reads config from environment.. if you want, you can just place your
# config here (see config.py.example), but i don't reccomend you to publish it
# then :)

import os

server = os.environ['CA_REDIS_SERVER']
port = int(os.environ['CA_REDIS_PORT'])
password = os.environ['CA_REDIS_PASSWORD']

def get_configjs():
    # uncomment next line and comment other lines if you want to read
    # plain config.js (example of it can be found in config.js.example)
    #return open('config.js', 'r').read()
    
    host = os.environ['CA_HOST']
    site_id = os.environ['CA_SITE_ID']
    return 'var rest_server = "{0}";\nvar site_id="{1}"'.format(host, site_id)
