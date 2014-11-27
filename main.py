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
from flask.ext.cors import CORS
from hashlib import md5

import db
import config

app = Flask(__name__)
cors = CORS(app, headers='Content-Type')

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
    page_uri_fixed = page_uri[len('root'):]
    return index().replace('<script src="config.js">', '<script language="javascript" type="text/javascript">\n//<--\n'+config.get_configjs(site_id, page_uri_fixed)+'//-->')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'status' : 'error', 'error': 'Not found' } ), 404)

COMMENT_FIELDS = ['nick', 'text', 'date', 'email', 'website',]

def get_comment(comment_id):
    r = {
        field : str(app.db.get('comment', comment_id, field), 'utf-8')
            for field in COMMENT_FIELDS
    }
    r['id'] = str(comment_id, 'utf-8')
    return r

@app.route('/get_comments/<string:site_id>/<path:page_uri>', methods=['GET'], strict_slashes=True)
def get_comments(site_id, page_uri=None):
    comment_ids = app.db.get_list('comments', site_id, page_uri)
    comments = [
        get_comment(comment_id)
            for comment_id in comment_ids
    ]
    return jsonify( { 'comments' : comments } )

def set_comment(cid, site_id, page_uri, pst):
    app.db.list_push(cid, 'comments', site_id, page_uri)
    post = {field : (pst[field] if field in pst else '') for field in COMMENT_FIELDS}
    app.db.set_dict(post, 'comment', cid)

@app.route('/add_comment/<string:site_id>/<path:page_uri>', methods=['POST'], strict_slashes=True)
def add_comment(site_id, page_uri):
    if not request.json:
        abort(400)
    
    comment_id = app.db.incr('total_count')
    set_comment(comment_id, site_id, page_uri, request.json)
    
    return jsonify({ 'status' : 'ok' }), 201

@app.route('/dump_comments/<string:site_id>', methods=['GET'])
def dump_comments(site_id):
    all_keys = app.db.request_all_keys()
    if all_keys != None:
        comments_keys = [key for key in all_keys if str(key, 'utf-8').startswith('comments:'+site_id+':')]
        comment_ids = {str(key, 'utf-8') : app.db.get_list(key) for key in comments_keys}
        comments = {db.unrid(key)[-1] : [get_comment(cid) for cid in comment_ids[key]] for key in comment_ids}
        return jsonify( { 'status' : 'ok', 'comments_dump' : comments } )
    else:
        return jsonify( { 'status' : 'processing' } )

@app.route('/undump_comments/<string:site_id>', methods=['POST'])
def undump_comments(site_id):
    if not request.json:
        abort(400)
    
    if md5(bytes(request.json['password'], 'utf-8')).hexdigest() != config.moderate_pass_hash:
        return jsonify( { 'status' : 'denied' } )
    
    print('restoring comments from dump')
    clear = request.json.get('clear', 'none')
    if clear == 'hard':
        clear_comments(site_id)
    
    dump = request.json['comments_dump']
    for page_uri in dump:
        if clear == 'soft':
            app.db.remove('comments', site_id, page_uri)
        for comment in dump[page_uri]:
            cid = comment.pop('id')
            set_comment(cid, site_id, page_uri, comment)
    
    return jsonify( { 'status' : 'ok' } )

@app.route('/remove_comment/<string:site_id>/<int:cid>/<path:page_uri>', methods=['POST'], strict_slashes=True)
def remove_comment(site_id, cid, page_uri):
    if not request.json:
        abort(400)
    
    if md5(bytes(request.json['password'], 'utf-8')).hexdigest() != config.moderate_pass_hash:
        return jsonify( { 'status' : 'denied' } )
    
    print('removing comment {0}'.format(cid))
    # remove comment from list
    removed = app.db.list_remove(cid, 0, 'comments', site_id, page_uri)
    if removed:
        # remove actual comment content
        app.db.remove_dict(COMMENT_FIELDS, 'comment', cid)
        status = 'ok'
    else:
        status = 'notfound'
    return jsonify( { 'status' : status } )

if __name__ == '__main__':
    from os import environ
    if 'CA_USE_CONFIG_JS' in environ:
        app.configjs = environ['CA_USE_CONFIG_JS']
    else:
        app.configjs = None
    app.db = db.open(config.server, config.port, config.password)
    if 'PORT' in environ:
        app.run(debug=False, host='0.0.0.0', port=int(environ['PORT']))
    else:
        app.run(debug=True)
