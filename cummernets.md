# Anime Controller

## Anime Controller - Deployment & Service

```python
kubectl apply -f anime_controller_deployment_service.yml
```

```python
kubectl get pods
```

```python
kubectl logs pod/{name_of_pod}
```

```python
kubectl get svc anime-controller # get CLUSTER-IP
```

```python
kubectl exec -it pod/{name_of_pod}
```

```python
wget -qO- http://{CLUSTER-IP}:50051/healthz
```

## Anime Controller - Scaler

```python
kubectl apply -f anime_controller_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa anime-controller-hpa
```

# Anime List

## Anime List - Deployment & Service

```python
kubectl apply -f anime_list_deployment_service.yml
```

```python
kubectl get pods
```

```python
kubectl logs pod/{name_of_pod}
```

## Anime List - Scaler

```python
kubectl apply -f anime_list_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa anime-list-hpa
```