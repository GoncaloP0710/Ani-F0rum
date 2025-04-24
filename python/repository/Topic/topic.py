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

        topic_map = {}

        topic_name_query = """
            SELECT topicname FROM `cn-fc58192.vmcloud.topics`;
        """
        topic_name_query_job = client.query(topic_name_query)
        topic_name_result = topic_name_query_job.result()

        for row in topic_name_result:
            try:
                topic_name = row['topicname']
                topic_map[topic_name] = {
                    "subscribers": [],
                    "publications": []
                }
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        subscribers_query = """
            SELECT
                t.topicname AS topic_name,
                s.name AS subscriber_name
            FROM `cn-fc58192.vmcloud.topics` t
            LEFT JOIN `cn-fc58192.vmcloud.subscribers` s ON t.topicid = s.topicid;
        """
        subscribers_query_job = client.query(subscribers_query)
        subscribers_result = subscribers_query_job.result()

        for row in subscribers_result:
            try:
                topic_name = row['topic_name']
                subscriber_name = row['subscriber_name']

                if topic_name in topic_map:
                    topic_map[topic_name]["subscribers"].append(Subscriber(name=subscriber_name))

            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")
                    
        message_publications_query = """
            SELECT
                t.topicname AS topic_name,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                m.username AS message_username,
                m.content AS message_content
            FROM `cn-fc58192.vmcloud.topics` t
            JOIN `cn-fc58192.vmcloud.publications` p ON t.topicid = p.topicid
            LEFT JOIN `cn-fc58192.vmcloud.messages` m ON p.publicationid = m.publicationid
        """
        message_publications_query_job = client.query(message_publications_query)
        message_publications_result = message_publications_query_job.result()

        for row in message_publications_result:
            try:
                topic_name = row['topic_name']
                publication_name = row['publication_name']
                publication_topicname = row['publication_topicname']
                message_username = row['message_username']
                message_content = row['message_content']

                if topic_name in topic_map:
                    publication = Publication(
                        name=publication_name,
                        topicname=publication_topicname,
                        message=Message(
                            username=message_username,
                            content=message_content
                        )
                    )
                    topic_map[topic_name]["publications"].append(publication)
            
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        image_publications_query = """
            SELECT
                t.topicname AS topic_name,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                i.name AS image_name,
                i.username AS image_username
            FROM `cn-fc58192.vmcloud.topics` t
            JOIN `cn-fc58192.vmcloud.publications` p ON t.topicid = p.topicid
            LEFT JOIN `cn-fc58192.vmcloud.images` i ON p.publicationid = i.publicationid
        """

        image_publications_query_job = client.query(image_publications_query)
        image_publications_result = image_publications_query_job.result()

        for row in image_publications_result:
            try:
                topic_name = row['topic_name']
                publication_name = row['publication_name']
                publication_topicname = row['publication_topicname']
                image_name = row['image_name']
                image_username = row['image_username']

                if topic_name in topic_map:
                    publication = Publication(
                        name=publication_name,
                        topicname=publication_topicname,
                        images=Image(
                            name=image_name,
                            username=image_username
                        )
                    )
                    topic_map[topic_name]["publications"].append(publication)
            
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        logging.info('Building Topics')
        
        topics = []
        for name, data in topic_map.items():
            logging.info(f'data: {data}')
            topics.append(Topic(
                topicname=name,
                subscribers=topic_map[name]["subscribers"],
                publications=topic_map[name]["publications"]
            ))

        logging.info(f"Fetched {len(topics)} topics from BigQuery")

        logging.info("Returning the response")

        return GetTopicsResponse(topics = topics) #if len(topics > 0) else NotFound("No topics found")
    
    def CreateTopic(self, request, context):

        logging.info("Processing a CreateTopic request")

        topic_name = request.topicname

        query = """
            INSERT INTO `cn-fc58192.vmcloud.topics` (topicid, topicname)
            SELECT
                IFNULL(MAX(topicid), 0) + 1 AS new_topicid,
                @topic_name AS topicname
            FROM `cn-fc58192.vmcloud.topics`
            WHERE NOT EXISTS (
                SELECT 1 FROM `cn-fc58192.vmcloud.topics` WHERE topicname = @topic_name
            );
            """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topic_name)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        result = query_job.result()

        logging.info(f"Succefully created {topic_name}")

        return CreateTopicResponse(topicname = topic_name)
    
    def GetTopic(self, request, context):

        logging.info("Processing a GetTopic request")

        topicname = request.topicname

        topic_map = {}

        topic_name_query = """
            SELECT topicname FROM `cn-fc58192.vmcloud.topics` t
            WHERE t.topicname = @topic_name;
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topicname)
            ]
        )

        topic_name_query_job = client.query(topic_name_query, job_config=job_config)
        topic_name_result = topic_name_query_job.result()

        for row in topic_name_result:
            try:
                topic_name = row['topicname']
                topic_map[topic_name] = {
                    "subscribers": [],
                    "publications": []
                }
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        subscribers_query = """
            SELECT
                t.topicname AS topic_name,
                s.name AS subscriber_name
            FROM `cn-fc58192.vmcloud.topics` t
            LEFT JOIN `cn-fc58192.vmcloud.subscribers` s ON t.topicid = s.topicid
            WHERE t.topicname = @topic_name;
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topicname)
            ]
        )

        subscribers_query_job = client.query(subscribers_query, job_config=job_config)
        subscribers_result = subscribers_query_job.result()

        for row in subscribers_result:
            try:
                topic_name = row['topic_name']
                subscriber_name = row['subscriber_name']

                if topic_name in topic_map:
                    topic_map[topic_name]["subscribers"].append(Subscriber(name=subscriber_name))

            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")
                    
        message_publications_query = """
            SELECT
                t.topicname AS topic_name,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                m.username AS message_username,
                m.content AS message_content
            FROM `cn-fc58192.vmcloud.topics` t
            JOIN `cn-fc58192.vmcloud.publications` p ON t.topicid = p.topicid
            LEFT JOIN `cn-fc58192.vmcloud.messages` m ON p.publicationid = m.publicationid
            WHERE t.topicname = @topic_name;
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topicname)
            ]
        )

        message_publications_query_job = client.query(message_publications_query, job_config=job_config)
        message_publications_result = message_publications_query_job.result()

        for row in message_publications_result:
            try:
                topic_name = row['topic_name']
                publication_name = row['publication_name']
                publication_topicname = row['publication_topicname']
                message_username = row['message_username']
                message_content = row['message_content']

                if topic_name in topic_map:
                    publication = Publication(
                        name=publication_name,
                        topicname=publication_topicname,
                        message=Message(
                            username=message_username,
                            content=message_content
                        )
                    )
                    topic_map[topic_name]["publications"].append(publication)
            
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        image_publications_query = """
            SELECT
                t.topicname AS topic_name,
                p.name AS publication_name,
                p.topicname AS publication_topicname,
                i.name AS image_name,
                i.username AS image_username
            FROM `cn-fc58192.vmcloud.topics` t
            JOIN `cn-fc58192.vmcloud.publications` p ON t.topicid = p.topicid
            LEFT JOIN `cn-fc58192.vmcloud.images` i ON p.publicationid = i.publicationid
            WHERE t.topicname = @topic_name;
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topicname)
            ]
        )

        image_publications_query_job = client.query(image_publications_query, job_config=job_config)
        image_publications_result = image_publications_query_job.result()

        for row in image_publications_result:
            try:
                topic_name = row['topic_name']
                publication_name = row['publication_name']
                publication_topicname = row['publication_topicname']
                image_name = row['image_name']
                image_username = row['image_username']

                if topic_name in topic_map:
                    publication = Publication(
                        name=publication_name,
                        topicname=publication_topicname,
                        images=Image(
                            name=image_name,
                            username=image_username
                        )
                    )
                    topic_map[topic_name]["publications"].append(publication)
            
            except KeyError as e:
                logging.error(f"Missing field in query result: {e}")
            except Exception as e:
                logging.error(f"Error processing row: {e}")

        logging.info('Building Topic')
        
        topic = None
        for name, data in topic_map.items():
            topic = Topic(
                topicname=name,
                subscribers=topic_map[name]["subscribers"],
                publications=topic_map[name]["publications"]
            )

        logging.info("Returning the topic")

        return GetTopicResponse(topic = topic)
    
    def PublishMessage(self, request, context):

        logging.info("Processing a PublishMessage request")

        topic_name = request.topicname
        publication_name = request.publicationname
        message = request.message
        username = message.username
        content = message.content

        query = """
            DECLARE topic_id INT64;
            DECLARE publication_id INT64;

            SET topic_id = (
                SELECT topicid FROM `cn-fc58192.vmcloud.topics`
                WHERE topicname = @topic_name
                LIMIT 1
            );

            SET publication_id = (
                SELECT IFNULL(MAX(publicationid), 0) + 1 FROM `cn-fc58192.vmcloud.publications`
            );

            INSERT INTO `cn-fc58192.vmcloud.publications` (publicationid, topicid, name, topicname)
            VALUES (publication_id, topic_id, @publication_name, @topic_name);

            INSERT INTO `cn-fc58192.vmcloud.messages` (publicationid, username, content)
            VALUES (publication_id, @username, @content);
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topic_name),
                bigquery.ScalarQueryParameter("publication_name", "STRING", publication_name),
                bigquery.ScalarQueryParameter("username", "STRING", username),
                bigquery.ScalarQueryParameter("content", "STRING", content)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        result = query_job.result()

        logging.info(f"Published: {publication_name}")

        return PublishInTopicResponse(publicationname = publication_name)
    
    def PublishImage(self, request, context):

        logging.info("Processing a PublishImage request")

        topic_name = request.topicname
        publication_name = request.publicationname
        image = request.image
        image_name = image.name
        username = image.username

        query = """
            DECLARE topic_id INT64;
            DECLARE publication_id INT64;

            SET topic_id = (
                SELECT topicid FROM `cn-fc58192.vmcloud.topics`
                WHERE topicname = @topic_name
                LIMIT 1
            );

            SET publication_id = (
                SELECT IFNULL(MAX(publicationid), 0) + 1 FROM `cn-fc58192.vmcloud.publications`
            );

            INSERT INTO `cn-fc58192.vmcloud.publications` (publicationid, topicid, name, topicname)
            VALUES (publication_id, topic_id, @publication_name, @topic_name);

            INSERT INTO `cn-fc58192.vmcloud.images` (publicationid, name, username)
            VALUES (publication_id, @image_name, @username);
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("topic_name", "STRING", topic_name),
                bigquery.ScalarQueryParameter("publication_name", "STRING", publication_name),
                bigquery.ScalarQueryParameter("username", "STRING", username),
                bigquery.ScalarQueryParameter("image_name", "STRING", image_name)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        result = query_job.result()

        logging.info(f"Published: {publication_name}")

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
