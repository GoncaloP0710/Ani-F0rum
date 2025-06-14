#!/bin/bash
# filepath: ./deploy.sh

# Set variables
CLUSTER_NAME="ani-cluster"
REGION="europe-west1"
PROJECT_ID="cn-fc58192"
SA_EMAIL="fc58192-service@cn-fc58192.iam.gserviceaccount.com"
K8S_SA="ani-f0rum-k8s"
DEPLOYMENT_DIR="./deployment_yml"

echo "Creating GKE cluster..."
gcloud container clusters create-auto $CLUSTER_NAME --region=$REGION

echo "Getting cluster credentials..."
gcloud container clusters get-credentials $CLUSTER_NAME --region=$REGION

echo "Current kubectl context:"
kubectl config current-context

echo "Updating cluster workload pool..."
gcloud container clusters update $CLUSTER_NAME \
  --region=$REGION \
  --workload-pool=$PROJECT_ID.svc.id.goog

echo "Adding IAM policy binding for BigQuery dataViewer..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_EMAIL" \
  --role="roles/bigquery.dataViewer"

echo "Creating Kubernetes service account..."
kubectl create serviceaccount $K8S_SA || echo "Service account may already exist."

echo "Binding IAM policy for workload identity user..."
gcloud iam service-accounts add-iam-policy-binding $SA_EMAIL \
  --member="serviceAccount:$PROJECT_ID.svc.id.goog[default/$K8S_SA]" \
  --role="roles/iam.workloadIdentityUser"

echo "Annotating Kubernetes service account with GCP service account..."
kubectl annotate serviceaccount \
  $K8S_SA \
  iam.gke.io/gcp-service-account=$SA_EMAIL --overwrite

echo "Deploying ingress-nginx controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.6.4/deploy/static/provider/cloud/deploy.yaml

echo "Applying Kubernetes deployments whithout entry_point_ingress.yml..."
find $DEPLOYMENT_DIR -type f ! -name 'entry_point_ingress.yml' -exec kubectl apply -f {} \;

echo "Waiting to start entry_point_ingress.yml..."
sleep 420

echo "Aplicando entry_point_ingress.yml..."
kubectl apply -f $DEPLOYMENT_DIR/entry_point_ingress.yml

echo "Getting ingress-nginx service info..."
kubectl get svc -n ingress-nginx

echo "Deployment script completed."