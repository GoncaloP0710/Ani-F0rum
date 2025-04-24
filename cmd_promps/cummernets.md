# Anime Controller

## Anime Controller - Deployment & Service

```python
kubectl apply -f python/controller/Anime/anime_controller_deployment_service.yml
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
kubectl exec -it pod/{name_of_pod} -- /bin/sh
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
kubectl apply -f python/others/AnimeList/anime_list_deployment_service.yml
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

# Anime Repository

## Anime Repository - Deployment & Service

```python
export API_TOKEN=$(cat JSON-KEY.json)
```

```python
kubectl apply -f python/repository/Anime/anime_repository_deployment_service.yml
```

## Anime Repository - Scaler

```python
kubectl apply -f anime_repository_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa anime-repository-hpa
```

# User Controller

## User Controller - Deployment & Service

```python
kubectl apply -f python/controller/Users/user_controller_deployment_service.yml
```

```python
kubectl get pods
```

```python
kubectl logs pod/{name_of_pod}
```

```python
kubectl get svc user-controller # get CLUSTER-IP
```

```python
kubectl exec -it pod/{name_of_pod} -- /bin/sh
```

```python
wget -qO- http://{CLUSTER-IP}:50040/healthz
```

## User Controller - Scaler

```python
kubectl apply -f python/controller/Users/user_controller_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa user-controller-hpa
```

# User Statistics

```python
kubectl apply -f python/others/UserStatistics/user_statistics_deployment_service.yml
```

# User Repository


```python
kubectl apply -f python/repository/User/user_repository_deployment_service.yml
```

# Feed Generator

# Achievement

```python
kubectl apply -f python/others/Achievements/achievements_deployment_service.yml
```

# User Recommendation

```python
kubectl apply -f python/others/UserRecommendations/user_recommendations_deployment_service.yml
```

# Topics Controller

## Topics Controller - Deployment & Service

```python
kubectl apply -f python/controller/Topics/topics_controller_deployment_service.yml
```

```python
kubectl get pods
```

```python
kubectl logs pod/{name_of_pod}
```

```python
kubectl get svc topics-controller # get CLUSTER-IP
```

```python
kubectl exec -it pod/{name_of_pod} -- /bin/sh
```

```python
wget -qO- http://{CLUSTER-IP}:50060/healthz
```

# GET /topics example
wget -qO- http://{CLUSTER-IP}:50060/topics

# GET /topics/{topic_name} example
wget -qO- http://{CLUSTER-IP}:50060/topics/yes

# POST /topics example
wget --post-data='{"name":"yes"}' --header='Content-Type: application/json' -qO- http://{CLUSTER-IP}:50060/topics

# POST /topics/{topic_name} example
wget --post-data='{"name":"sim", "topic_name":"yes", "message":{"username":"gajo","content":"no"}}' --header='Content-Type: application/json' -qO- http://{CLUSTER-IP}:50060/topics/yes

## Topics Controller - Scaler

```python
kubectl apply -f topics_controller_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa topics-controller-hpa
```

# Publisher

## Publisher - Deployment & Service

```python
kubectl apply -f python/others/Publisher/publisher_deployment_service.yml
```

```python
kubectl get pods
```

```python
kubectl logs pod/{name_of_pod}
```

## Publisher - Scaler

```python
kubectl apply -f python/others/Publisher/publisher_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa publisher-hpa
```

# Topic Repository

## Topic Repository - Deployment & Service

```python
kubectl apply -f python/repository/Topic/topic_repository_deployment_service.yml
```

## Topic Repository - Scaler

```python
kubectl apply -f python/repository/Topic/topic_repository_scaler.yml
```

```python
kubectl get hpa
```

```python
kubectl describe hpa topic-repository-hpa
```