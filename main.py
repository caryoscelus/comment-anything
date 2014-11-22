#! /usr/bin/env python3

#
#  Copyright (C) 2014 caryoscelus
#  
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#  
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os
from flask import Flask, jsonify, make_response, abort, request
import redis
import config

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    i = open('index.html', 'r').read()
    return i

@app.route('/main.js', methods=['GET'])
def mainjs():
    i = open('main.js', 'r').read()
    return i

@app.route('/config.js', methods=['GET'])
def configjs():
    if app.configjs:
        i = open(app.configjs, 'r').read()
        return i
    return config.get_configjs(None, '/')

@app.route('/iframe/<string:site_id>/<path:page_uri>', methods=['GET'], strict_slashes=True)
def iframe(site_id, page_uri):
    return index().replace('<script src="config.js">', '<script language="javascript" type="text/javascript">\n//<--\n'+config.get_configjs(site_id, page_uri)+'//-->')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'status' : 'error', 'error': 'Not found' } ), 404)

COMMENT_FIELDS = ['nick', 'text', 'date', 'email', 'website',]

def get_comment_content(r, comment_id, whats):
    return dict([
        (what, str(r.get('comment:'+str(comment_id, 'utf-8')+':'+what), 'utf-8'))
            for what in whats])

def set_comment_content(r, comment_id, whats, content):
    for what in whats:
        value = ''
        if what in content:
            value = content[what]
        r.set('comment:'+str(comment_id)+':'+what, value)

@app.route('/get_comments/<string:site_id>/<path:page_uri>', methods=['GET'], strict_slashes=True)
def get_comments(site_id, page_uri=None):
    r = redis.Redis(host=config.server, port=config.port, password=config.password)
    length = r.llen('comments:'+site_id+':'+page_uri)
    comment_ids = r.lrange('comments:'+site_id+':'+page_uri, 0, length-1)
    comments = [
        get_comment_content(r, comment_id, COMMENT_FIELDS)
            for comment_id in comment_ids
    ]
    return jsonify( { 'comments' : comments } )

@app.route('/add_comment/<string:site_id>/<path:page_uri>', methods=['POST'], strict_slashes=True)
def add_comment(site_id, page_uri):
    if not request.json:
        abort(400)
    
    r = redis.Redis(host=config.server, port=config.port, password=config.password)
    comment_id = r.incr('total_count')
    r.rpush('comments:'+site_id+':'+page_uri, comment_id)
    set_comment_content(r, comment_id, COMMENT_FIELDS, request.json)
    return jsonify({ 'status' : 'ok' }), 201

if __name__ == '__main__':
    from os import environ
    if 'CA_USE_CONFIG_JS' in environ:
        app.configjs = environ['CA_USE_CONFIG_JS']
    else:
        app.configjs = None
    if 'PORT' in environ:
        app.run(debug=False, host='0.0.0.0', port=int(environ['PORT']))
    else:
        app.run(debug=True)
