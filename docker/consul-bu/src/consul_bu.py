#!/usr/bin/env python

import os
import json
import requests
import logging
import boto3
import datetime
from flask import Flask, jsonify, request, Response
from functools import wraps

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

bucket = os.getenv('BUCKET', 'cheapandsalty')
region = os.getenv('REGION', 'us-east-1')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
port = os.getenv('PORT', 3000)
debug = os.getenv('DEBUG', False)
consul_addr = os.getenv('CONSUL_ADDR', 'http://127.0.0.1:8500')
interval = os.getenv('INTERVAL', 86400)
tmp_file = '/tmp/snapshot.tgz'

app = Flask(__name__)
s3 = boto3.client(
  's3',
  aws_access_key_id = aws_access_key_id,
  aws_secret_access_key = aws_secret_access_key,
)

def check_auth(username, password):
  headers = {'content-type': 'application/json'}
  url = "{0}/v1/auth/userpass/login/{1}".format(vault_addr, username)
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
  r = requests.get("{0}/v1/snapshot".format(consul_addr))
  with open(tmp_file, 'wb') as code:
    code.write(r.content)
  now = datetime.datetime.now()
  key = "consul-bu/{0}-snapshot.tgz".format(now.strftime("%Y-%m-%d"))
  s3.upload_file(key, bucket, tmp_file)
  os.remove(tmp_file)

@app.route('/healthz', methods=['GET'])
def healthz():
  return json.dumps({'status':'ok'}), 200, {'ContentType':'application/json'}

@app.route('/', methods=['GET'])
@requires_auth
def trigger():
  return backup_consul()

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=port, debug=debug)
  while True:
    backup_consul()
    time.sleep(int(interval))
