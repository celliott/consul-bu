#!/usr/bin/env python

import os

def get_options():
  return {
    'bucket': os.getenv('BUCKET', 'cheapandsalty'),
    'region': os.getenv('REGION', 'us-east-1'),
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'port': os.getenv('PORT', 3000),
    'debug': os.getenv('DEBUG', False),
    'consul_addr': os.getenv('CONSUL_ADDR', 'http://127.0.0.1:8500'),
    'vault_addr': os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200'),
    'interval': os.getenv('INTERVAL', 86400),
    'tmp_file': '/tmp/snapshot.tgz',
  }
