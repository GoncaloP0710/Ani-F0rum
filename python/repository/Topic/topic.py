import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import random
from concurrent import futures

import grpc

from python.repository.Topic.TopicRepository_pb2_grpc import (
    PublisherServicer,
    add_TopicServicer_to_server,
)

from python.repository.Topic.TopicRepository_pb2 import (
    MostUsedTopicsResponse,
    TopicSubscribersResponse,
    RecomendationResponse,
    GetTopicsResponse,
    CreateTopicResponse,
    GetTopicResponse,
    PublishInTopicResponse,
    KarmaResponse
)

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound, BadRequest
from topic_pb2 import (
    Subscriber,
    Message,
    Image,
    Publication,
    Topic,
    MostUsedTopicsResponse,
    TopicSubscribersResponse,
    RecomendationResponse,
    GetTopicsResponse,
    CreateTopicResponse,
    GetTopicResponse,
    PublishInTopicResponse,
    KarmaResponse
)

class PublishService(PublisherServicer):

    def MostUsedTopics(self, request, context):
        
        print("Processing a MostUsedTopics request")
        micro_service_response = []
        print("Received response from other micro service")
        trending_topics = [Topic(n) for n in micro_service_response] # interagir com o próximo microserviço
        print("Returning the response: " + trending_topics)

        return MostUsedTopicsResponse(trending_topics)
    
    def TopicSubscribers(self, request, context):

        print("Processing a TopicSubscribers request")
        
        res = []

        for topic_name in request.topicnames:
            
            micro_service_response = []
            print("Received response from other micro service for topic name: " + topic_name)
            subscribers = [Subscriber() for n in micro_service_response] # interagir com o próximo microserviço
            res.append(subscribers)

        print("Returning the response: " + res)
        return TopicSubscribersResponse(subscribers)

    def Recomendation(self, request, context):

        print("Processing a Recomendation request")
        
        theme = request.theme

        micro_service_response = []
        print("Received response from other micro service")
        publication_names = [Publication() for n in micro_service_response] # interagir com o próximo microserviço

        print("Returning the response: " + publication_names)

        return RecomendationResponse(publication_names)

    def GetTopics(self, request, context):

        print("Processing a GetTopics request")

        micro_service_response = []
        print("Received response from other micro service")
        topics = [Topic(n) for n in micro_service_response] # interagir com o próximo microserviço

        print("Returning the response: " + topics)

        return GetTopicsResponse(topics)
    
    def CreateTopic(self, request, context):

        print("Processing a GetTopics request")

        micro_service_response = 'topicname'
        print("Received response from other micro service")
        res = micro_service_response

        print("Returning the response: " + res)

        return CreateTopicResponse(res)
    
    def GetTopic(self, request, context):

        topic_name = request.topicname

        micro_service_response = Topic()
        print("Received response from other micro service")
        topic = micro_service_response

        print("Returning the response: " + topic)

        return GetTopicResponse(topic)
    
    def PublishInTopic(self, request, context):

        print("Processing a PublishInTopic request")

        user_id = request.userId
        topic_name = request.topicname
        content = request.content

        if isinstance(content, Message):

            micro_service_response = Topic()
            print("Received response from other micro service")
            topic = micro_service_response
            
        elif isinstance(content, Image):

            micro_service_response = Topic()
            print("Received response from other micro service")
            topic = micro_service_response
    
        else:
            raise BadRequest("Invalid content of publication")

        print("Returning the response: " + topic)

        return PublishInTopicResponse(topic)
    
    def Karma(self, request, context):
        topic_name = request.topicname
        user_id = request.userId

        micro_service_response = Topic()
        print("Received response from other micro service")
        topic = micro_service_response

        print("Returning the response: " + topic)

        return KarmaResponse(topic)
        

"""
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            raise NotFound("Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        return RecommendationResponse(topic=books_to_recommend)
"""

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_TopicServicer_to_server(
        PublishService(), server
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

    server.add_insecure_port("[::]:50060")
    server.start()
    print('Topic Repository server running on port 50060')
    server.wait_for_termination()

if __name__ == "__main__":
    serve()