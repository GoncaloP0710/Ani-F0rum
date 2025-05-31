# tutorial do secret

To begin you need to investigate what permissions will be required by the app at:
https://cloud.google.com/bigquery/docs/access-control

Now looking at the list of service accounts select the action “Manage keys” for the service account
that you just created. Select “Add Key”, type JSON. Download the JSON file with the private key.
Upload the JSON file (JSON-KEY.json) to cloud shell.

Create an environment variable called API_TOKEN with
$ export API_TOKEN=$(cat JSON-KEY.json)

Add the following imports,
from google.oauth2 import service_account
import json, os

and replace the line,
client = bigquery.Client(location="europe-west4")

by the following four lines
json_string = os.environ.get('API_TOKEN')
json_file = json.loads(json_string)
credentials = service_account.Credentials.from_service_account_info(json_file)
client = bigquery.Client(credentials=credentials, location="europe-west4")

Make sure that the API_TOKEN environment variable is defined for the current terminal and run you
the container with:
$ docker run -it --rm -e API_TOKEN --name bigquery -p 8080:8080 bigquery:latest

Upload the container image that you just created to some registry (DockerHub, GCR …).
Start the minikube from the Cloud Code.
Create the secret from the JSON file with the key, you can use the following command:
$ kubectl create secret generic BigSecret --from-literal "API_TOKEN=$(cat JSON-KEY.json)"

# tutorial do cluster

https://moodle.ciencias.ulisboa.pt/pluginfile.php/581842/mod_resource/content/8/CC2425-TP05-Kubernetes.pdf

slide 10-11