# Cluster Commands
```python
gcloud container clusters create-auto ani-cluster --region=europe-west1
```

```python
gcloud container clusters get-credentials ani-cluster --region=europe-west1
```

```python
kubectl apply \
 -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml
```

```python
kubectl config current-context
```

```python
gcloud container clusters update ani-cluster \
  --region=europe-west1 \
  --workload-pool=cn-fc58192.svc.id.goog
```

```python
export SA_EMAIL=fc58192-service@cn-fc58192.iam.gserviceaccount.com
```

```python
gcloud projects add-iam-policy-binding cn-fc58192 \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/bigquery.dataViewer"
```

```python
kubectl create serviceaccount ani-f0rum-k8s
```

```python
gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \
  --member="serviceAccount:cn-fc58192.svc.id.goog[default/ani-f0rum-k8s]" \
  --role="roles/iam.workloadIdentityUser"
```

```python
kubectl annotate serviceaccount \
  ani-f0rum-k8s \
  iam.gke.io/gcp-service-account=$SA_EMAIL
```


```python
kubectl apply -f ./deployment_yml/
```

```python
kubectl get svc -n ingress-nginx
```

```python
gcloud container clusters delete ani-cluster --region=europe-west1
```