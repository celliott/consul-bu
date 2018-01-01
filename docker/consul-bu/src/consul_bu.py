#!/usr/bin/env python

import os
import json
import time
import boto3
import logging
import options
import requests
import datetime
from flask import Flask, request, Response
from functools import wraps

options = options.get_options()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
s3 = boto3.resource('s3',
  aws_access_key_id=options['aws_access_key_id'],
  aws_secret_access_key=options['aws_secret_access_key'],
  region_name=options['aws_default_region'])

def ok():
  return json.dumps({'status':'ok'}), 200, {'ContentType':'application/json'}

def err(e):
  logger.error(e)
  return json.dumps({'status':'error', 'msg': e}), 500, {'ContentType':'application/json'}

def check_auth(username, password):
  """Uses vault userpass for auth. See readme"""
  url = "{0}/v1/auth/userpass/login/{1}".format(options['vault_addr'], username)
  headers = {'content-type': 'application/json'}
  data = { "password": password }
  try:
    r = requests.post(url, headers=headers, data=json.dumps(data))
    response = json.loads(r.text)
    if response['auth']['client_token']:
      logger.info("{} has been authenticated".format(username))
      return True
  except:
    pass

def authenticate():
  return Response(
  'Login Required', 401,
  {'WWW-Authenticate': 'Basic realm="Login Required"'})

def auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
      return authenticate()
    return f(*args, **kwargs)
  return decorated

def upload():
  """Uploads snapshot to s3"""
  now = datetime.datetime.now()
  key = "consul-bu/{0}-snapshot.tgz".format(now.strftime("%Y-%m-%d"))
  try:
    s3.meta.client.upload_file(options['tmp_file'], options['s3_bucket'], key)
    os.remove(options['tmp_file'])
except e:
    err(e)
    exit(1)

def backup():
  """Gets snapshot from consul http endpoint"""
  try:
    r = requests.get("{0}/v1/snapshot".format(options['consul_addr']))
    with open(options['tmp_file'], 'wb') as f:
      f.write(r.content)
    upload()
  except e:
    err(e)
    exit(1)

@app.route('/healthz', methods=['GET'])
def healthz():
  return ok()

@app.route('/', methods=['GET'])
@auth
def trigger():
  backup()
  return ok()

if __name__ == "__main__":
  while True:
    backup()
    try:
      app.run(host='0.0.0.0', port=options['port'], debug=options['debug'])
    except:
      pass
    time.sleep(int(options['interval']))
