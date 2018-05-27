# vault
A container to backup consul to s3. Backup runs on interval and has http trigger with auth.


Next steps:
* Improve error handling
* Get temp AWS creds from vault

## Usage
Build and push container

```
$ make push
```

### Helm chart
NOTE depends on [nginx-ingress](https://github.com/kubernetes/charts/tree/master/stable/nginx-ingress), [external-dns](https://github.com/kubernetes/charts/tree/master/stable/external-dns), and [kube-lego](https://github.com/kubernetes/charts/tree/master/stable/kube-lego)

#### Helm Deployment
Set config and secrets in values.yaml

```yaml
consul:
  address: http://consul-consul.vault:8500
  backup_interval: 86400
aws:
  access_key: <access_key>
  secret_key: <secret_key>
  s3_bucket: <s3_bucket>
```

```bash
$ make deploy
```

#### Delete

```bash
$ make delete
```

#### Remote trigger
NOTE uses vault userpass for auth

```bash
$ vault auth-enable userpass
$ vault write auth/userpass/users/${VAULT_USER} \
  password=${VAULT_PASS} \
  policies=default
```

```bash
$ curl -u ${VAULT_USER}:${VAULT_PASS} https://${SERVICE}.${DOMAIN}
```
