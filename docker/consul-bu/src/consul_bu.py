#!/usr/bin/env python

import os
import json
import time
import boto3
import logging
import options
import requests
import datetime
from flask import Flask, jsonify, request, Response
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
options = options.get_options()

app = Flask(__name__)
s3 = boto3.resource('s3',
  aws_access_key_id=options['aws_access_key_id'],
  aws_secret_access_key=options['aws_secret_access_key'],
  region_name=options['region'])

def check_auth(username, password):
  """Uses vault userpass for auth. See readme"""
  headers = {'content-type': 'application/json'}
  url = "{0}/v1/auth/userpass/login/{1}".format(options['vault_addr'], username)
  data = { "password": password }
  r = requests.post(url, headers=headers, data=json.dumps(data))
  response = json.loads(r.text)
  try:
    if response['auth']['client_token']:
      return True
  except:
    pass

def authenticate():
  return Response(
  'Login Required', 401,
  {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

def backup_consul():
  """Gets snapshot from consul http endpoint and copies to s3 bucket"""
  r = requests.get("{0}/v1/snapshot".format(options['consul_addr']))
  with open(options['tmp_file'], 'wb') as code:
    code.write(r.content)
  now = datetime.datetime.now()
  key = "consul-bu/{0}-snapshot.tgz".format(now.strftime("%Y-%m-%d"))
  s3.meta.client.upload_file(options['tmp_file'], options['bucket'], key)
  os.remove(options['tmp_file'])

@app.route('/healthz', methods=['GET'])
def healthz():
  return json.dumps({'status':'ok'}), 200, {'ContentType':'application/json'}

@app.route('/', methods=['GET'])
@requires_auth
def trigger():
  backup_consul()
  return json.dumps({'status':'ok'}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
  while True:
    backup_consul()
    app.run(host='0.0.0.0', port=options['port'], debug=options['debug'])
    time.sleep(int(options['interval']))
