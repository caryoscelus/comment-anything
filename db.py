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

'''
This is helper module to abstract redis db operations.
It is recommended to only use open() and class methods.
'''

import redis
from threading import Thread

def stringify(b):
    if type(b) == 'str':
        return b
    elif type(b) == 'bytes':
        return str(b, 'utf-8')
    else:
        return str(b)

def rid(args):
    return ':'.join([stringify(arg) for arg in args])

def get_all_keys(self):
    self.get_all_keys()

class RedisWrapper:
    'Wrapper for Redis db connection'
    def __init__(self, r):
        self.r = r
        self.all_keys_cache = None
        self.all_keys_lock = False
    
    def get(self, *addr):
        'Get single value'
        self.r.get(rid(addr))
    
    def get_list(self, *addr):
        'Get full list'
        l = self.r.llen(rid(addr))
        return self.r.lrange(rid(addr), 0, l-1)
    
    def set(self, value, *addr):
        return self.r.set(rid(addr), value)
    
    def remove(self, *addr):
        return self.r.delete(rid(addr))
    
    def incr(self, *addr):
        'Increase int variable'
        return self.r.incr(rid(addr))
    
    def list_push(self, elem, *addr):
        'push element to list (rpush)'
        return self.r.rpush(rid(addr), elem)
    
    def list_remove(self, elem, d, *addr):
        return self.r.lrem(rid(addr), elem, d)
    
    def set_dict(self, d, *addr):
        'Set dictionary..'
        base = rid(addr)
        for key in d:
            self.set(d[key], base, key)
    
    def remove_dict(self, keys, *addr):
        for key in keys:
            self.remove(rid(addr), key)
    
    def get_all_keys(self):
        self.all_keys_lock = True
        nxt = 0
        keys = []
        while True:
            nxt, part = self.r.scan(nxt)
            keys += part
            # old redis wrapper returned raw bytes instead of int
            if int(nxt) == 0:
                break
        self.all_keys_cache = keys
        self.all_keys_lock = False
    
    def request_all_keys(self):
        'If keys are cached, return them, otherwise start caching.'
        if self.all_keys_cache:
            return self.all_keys_cache
        
        if not self.all_keys_lock:
            Thread(target=get_all_keys, args=(self,)).start()
        
        return None

def open(host, port, password):
    'Open database connection.'
    return RedisWrapper(redis.Redis(host=host, port=port, password=password))
