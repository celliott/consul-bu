#!/usr/bin/env python

import os

def get_options():
  return {
    'aws_default_region': os.getenv('AWS_DEFAULT_REGION', 'us-east-1'),
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    's3_bucket': os.getenv('S3_BUCKET'),
    'port': os.getenv('PORT', 3000),
    'debug': os.getenv('DEBUG', False),
    'consul_addr': os.getenv('CONSUL_ADDR', 'http://127.0.0.1:8500'),
    'vault_addr': os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200'),
    'interval': os.getenv('INTERVAL', 86400),
    'tmp_file': 'snapshot.tgz',
  }
