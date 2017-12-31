# vault
A container to backup consul to s3. Backup runs on interval and has http trigger with auth.

## Usage
* Build and push container

```
$ make push
```

### Helm chart
NOTE depends on [nginx-ingress](https://github.com/kubernetes/charts/tree/master/stable/nginx-ingress), [external-dns](https://github.com/kubernetes/charts/tree/master/stable/external-dns), and [kube-lego](https://github.com/kubernetes/charts/tree/master/stable/kube-lego)

#### Deploy
Set config and secrets in values.yaml

```
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
