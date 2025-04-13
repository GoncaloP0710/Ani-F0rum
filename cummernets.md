
# Anime Controller - Deployment & Service

kubectl apply -f anime_controller_deployment_service.yml

kubectl get pods

kubectl logs pod/

# Anime Controller - Scaler

kubectl apply -f anime_controller_scaler.yml

kubectl get hpa

kubectl describe hpa anime-controller-hpa