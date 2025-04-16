import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import random
from collections import Counter
from concurrent import futures

# ---------------------------------------------------------------
from concurrent import futures
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
# ---------------------------------------------------------------

import grpc

from python.repository.Topic.TopicRepository_pb2_grpc import (
    TopicRepositoryServicer,
    add_TopicRepositoryServicer_to_server,
)

from python.repository.Topic.TopicRepository_pb2 import (
    MostUsedTopicsResponse,
    TopicSubscribersResponse,
    RecomendationResponse,
    GetTopicsResponse,
    CreateTopicResponse,
    GetTopicResponse,
    PublishInTopicResponse,
)

from python.Common.Topic_pb2 import (
    Subscriber,
    Message,
    Image,
    Publication,
    Topic,
)

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from google.cloud import bigquery
import logging

logging.basicConfig(
    level=logging.INFO,  # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
    handlers=[
        logging.StreamHandler()  # Output logs to the console
    ]
)

client = bigquery.Client(project="cn-fc58192", location="europe-west1")

class TopicService(TopicRepositoryServicer):

    def __init__(self):
        self.Topics = [
            Topic(
                topicname = 'Solo Leveling ep12',
                subscribers = [
                    Subscriber(name = 'Diogo'),
                    Subscriber(name = 'Gonçalo'),
                    Subscriber(name = 'André'),
                    Subscriber(name = 'Daniel')
                ],
                publications = [
                    Publication(
                        name = "Diogo Reaction",
                        topicname = 'Solo Leveling',
                        message = Message(
                            username = 'Diogo',
                            content = 'Wow, it was amazing!'
                        )
                    ),
                    Publication(
                        name = 'Answer to Diogo Reaction',
                        topicname = 'Solo Leveling',
                        message = Message(
                            username = 'Gonçalo',
                            content = 'I agree Gajo.'
                        )
                    )
                ]
            ),
            Topic(
                topicname = 'Solo Leveling images',
                subscribers = [
                    Subscriber(name = 'Diogo'),
                    Subscriber(name = 'Gonçalo'),
                    Subscriber(name = 'André'),
                    Subscriber(name = 'Daniel')
                ],
                publications = [
                    Publication(
                        name = 'Last fight',
                        topicname = 'Solo Leveling',
                        images = Image(
                            name = 'Epic fight',
                            username = 'Diogo'
                        )
                    )
                ]
            )
        ]

    def Recomendation(self, request, context):

        print("Processing a Recomendation request")
        
        theme = request.theme

        micro_service_response = []
        print("Received response from other micro service")
        publication_names = [Publication() for n in micro_service_response] # interagir com o próximo microserviço

        print("Returning the response: " + publication_names)

        return RecomendationResponse(publication_names)

    def GetTopics(self, request, context):

        logging.info("Processing a GetTopics request")

        query = """
            SELECT
                t.topicname AS topic_name,
                s.name AS subscriber_name,
                p.publicationid,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                m.username AS message_username,
                m.content AS message_content,
                NULL AS image_name,
                NULL AS image_username
            FROM topics t
            LEFT JOIN subscribers s ON t.topicid = s.topicid
            LEFT JOIN publications p ON t.topicid = p.topicid
            LEFT JOIN messages m ON p.publicationid = m.publicationid

            UNION ALL

            SELECT
                t.topicname AS topic_name,
                s.name AS subscriber_name,
                p.publicationid,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                NULL AS message_username,
                NULL AS message_content,
                i.name AS image_name,
                i.username AS image_username
            FROM topics t
            LEFT JOIN subscribers s ON t.topicid = s.topicid
            LEFT JOIN publications p ON t.topicid = p.topicid
            LEFT JOIN images i ON p.publicationid = i.publicationid
            """
        
        query_job = client.query(query)
        result = query_job.result()

        logging.info('Building Topics')

        topic_map = {}

        for row in result:
            try:
            
                name = row['topic_name']
                subscriber_name = row.get('subscriber_name')

                if name not in topic_map:
                    topic_map[name] = {
                        "subscribers": set(),
                        "publications": []
                    }

                if subscriber_name:
                    topic_map[name]["subscribers"].add(subscriber_name)

                if row['message_username'] is not None:
                    publication = Publication(
                        name=row['publication_name'],
                        topicname=row['publication_topicname'],
                        message = Message(
                            username=row['message_username'],
                            content=row['message_content']
                        )
                    )
                    
                elif row['image_name'] is not None:
                    publication = Publication(
                        name=row['publication_name'],
                        topicname=row['publication_topicname'],
                        images = Image(
                            name=row['image_name'],
                            username=row['image_username']
                        )
                    )
                else:
                    continue

                topic_map[name]["publications"].append(publication)

                topics = []
                for name, data in topic_map.items():
                    topics.append(Topic(
                        name=name,
                        subscribers=list(data["subscribers"]),
                        publications=list(data["publications"])
                    ))

            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        logging.info(f"Fetched {len(topics)} topics from BigQuery")

        logging.info("Returning the response")

        return GetTopicsResponse(topics = topics) #if len(topics > 0) else NotFound("No topics found")
    
    def CreateTopic(self, request, context):

        logging.info("Processing a CreateTopic request")

        topic_name = request.topicname

        query = """
            INSERT INTO topics (topicid, topicname)
            SELECT
                IFNULL(MAX(topicid), 0) + 1 AS new_topicid,
                @topic_name AS topicname
            FROM topics
            WHERE NOT EXISTS (
            SELECT 1 FROM topics WHERE topicname = @topic_name
            );
            """
        
        query_job = client.query(query)
        result = query_job.result()

        logging.info(f"Succefully created {topic_name}")

        return CreateTopicResponse(topicname = topic_name)
    
    def GetTopic(self, request, context):

        print("Processing a GetTopic request")

        topicname = request.topicname

        query = """
            SELECT
                t.topicname AS topic_name,
                s.name AS subscriber_name,
                p.publicationid,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                m.username AS message_username,
                m.content AS message_content,
                NULL AS image_name,
                NULL AS image_username
            FROM topics t
            LEFT JOIN subscribers s ON t.topicid = s.topicid
            LEFT JOIN publications p ON t.topicid = p.topicid
            LEFT JOIN messages m ON p.publicationid = m.publicationid
            WHERE t.topicname = @topicname

            UNION ALL

            SELECT
                t.topicname AS topic_name,
                s.name AS subscriber_name,
                p.publicationid,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                NULL AS message_username,
                NULL AS message_content,
                i.name AS image_name,
                i.username AS image_username
            FROM topics t
            LEFT JOIN subscribers s ON t.topicid = s.topicid
            LEFT JOIN publications p ON t.topicid = p.topicid
            LEFT JOIN images i ON p.publicationid = i.publicationid
            WHERE t.topicname = @topicname
            """
        
        query_job = client.query(query)
        result = query_job.result()

        logging.info('Building Topics')

        topic_map = {}

        for row in result:
            try:
            
                name = row['topic_name']
                subscriber_name = row.get('subscriber_name')

                if name not in topic_map:
                    topic_map[name] = {
                        "subscribers": set(),
                        "publications": []
                    }

                if subscriber_name:
                    topic_map[name]["subscribers"].add(subscriber_name)

                if row['message_username'] is not None:
                    publication = Publication(
                        name=row['publication_name'],
                        topicname=row['publication_topicname'],
                        message = Message(
                            username=row['message_username'],
                            content=row['message_content']
                        )
                    )
                    
                elif row['image_name'] is not None:
                    publication = Publication(
                        name=row['publication_name'],
                        topicname=row['publication_topicname'],
                        images = Image(
                            name=row['image_name'],
                            username=row['image_username']
                        )
                    )
                else:
                    continue

                topic_map[name]["publications"].append(publication)

                topics = []
                for name, data in topic_map.items():
                    topics.append(Topic(
                        name=name,
                        subscribers=list(data["subscribers"]),
                        publications=list(data["publications"])
                    ))

            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        micro_service_response = Topic()
        print("Received response from other micro service")
        topic = None
        for t in self.Topics:
            if t.topicname == topic_name:
                topic = t
                break

        print("Returning the response")

        return GetTopicResponse(topic = topic)
    
    def PublishMessage(self, request, context):

        print("Processing a PublishMessage request")

        topic_name = request.topicname
        publication_name = request.publicationname
        message = request.message

        print(topic_name)
        print(publication_name)
        print(message.username)
        print(message.content)
        
        print('size')
        print(len(self.Topics))

        for topic in self.Topics:
            print(topic.topicname)
            print(topic_name)
            if topic.topicname == topic_name:
                micro_service_response = Topic()
                print("Received response from other micro service")
                topic.publications.append(
                    Publication(
                        name = publication_name,
                        topicname = topic_name,
                        message = Message(
                            username = message.username,
                            content = message.content,
                        )
                    )
                )
                break
                 
        print("Returning the response: ")
        print(publication_name)

        return PublishInTopicResponse(publicationname = publication_name)
    
    def PublishImage(self, request, context):

        print("Processing a PublishImage request")

        topic_name = request.topicname
        publication_name = request.publicationname
        image = request.image

        for topic in self.Topics:
            if topic.name == topic_name:
                micro_service_response = Topic()
                print("Received response from other micro service")
                topic.publications.append(
                    Publication(
                        name = publication_name,
                        topicname = topic_name,
                        images = Image(
                            name = image.name,
                            username = image.username,
                        )
                    )
                )
                 
        print("Returning the response: " + publication_name)

        return PublishInTopicResponse(publicationname = publication_name)

# ----------------------------------------------------------------
# HTTP server for Kubernetes probes
class ProbeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/healthz", "/readiness", "/startup"]:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def start_http_server():
    http_server = HTTPServer(('0.0.0.0', 8080), ProbeHandler)
    print("HTTP server for probes started on port 8080")
    http_server.serve_forever()
# ----------------------------------------------------------------

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_TopicRepositoryServicer_to_server(
        TopicService(), server
    )

    """
    with open("server.key", "rb") as fp:
        server_key = fp.read()
    with open("server.pem", "rb") as fp:
        server_cert = fp.read()
    with open("ca.pem", "rb") as fp:
        ca_cert = fp.read()

    creds = grpc.ssl_server_credentials(
        [(server_key, server_cert)],
        root_certificates=ca_cert,
        require_client_auth=True,
    )
    """

    server.add_insecure_port("[::]:50062")
    server.start()
    print('Topic Repository server running on port 50062')

    # -------------------------------------------------
    # Start the HTTP server for probes in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    server.wait_for_termination()

if __name__ == "__main__":
    serve()
