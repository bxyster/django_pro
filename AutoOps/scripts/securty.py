#!/usr/bin/env python
#coding:utf8

import time
import hashlib

def create_api_key():
	hash_obj = hashlib.md5()
	key = '&W0@6M9HXm05viBx' 
	time_span = time.time()
	hash_obj.update("%s/%f" % (key,time_span))
	encryption = hash_obj.hexdigest()
	result = "%s/%f" % (encryption,time_span)
	return result
