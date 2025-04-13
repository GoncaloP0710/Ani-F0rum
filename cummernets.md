
# Anime Controller - Deployment & Service

```python
kubectl apply -f anime_controller_deployment_service.yml
```

```python
kubectl get pods
```

```python
kubectl logs pod/{name_of_pod}
```

# Anime Controller - Scaler

```python
kubectl apply -f anime_controller_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa anime-controller-hpa
```