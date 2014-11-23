# this reads config from environment.. if you want, you can just place your
# config here (see config.py.example), but i don't reccomend you to publish it
# then :)

from os import environ

server = environ['CA_REDIS_SERVER']
port = int(environ['CA_REDIS_PORT'])
password = environ['CA_REDIS_PASSWORD']
try:
    moderate_pass_hash = environ['CA_MODERATE_PASS_HASH']
except KeyError:
    moderate_pass_hash = None

def get_configjs(site_id, page_uri):
    # uncomment next line and comment other lines if you want to read
    # plain config.js (example of it can be found in config.js.example)
    #return open('config.js', 'r').read()
    
    host = environ.get('CA_HOST', 'http://localhost:5000/')
    if not site_id:
        site_id = environ.get('CA_SITE_ID', 'test')
    
    return 'var rest_server = "{0}"\nvar site_id="{1}"\nvar current_path="{2}"'.format(host, site_id, page_uri)
