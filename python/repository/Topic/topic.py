import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import random
from collections import Counter
from concurrent import futures

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

    def MostUsedTopics(self, request, context):
        
        print("Processing a MostUsedTopics request")
        micro_service_response = [] # TODO with SQL
        print("Received response from other micro service")

        # assume that the anime name are the first 2 words
        anime_names = [" ".join(topic.topicname.split()[:2]) for topic in self.Topics]
        counter = Counter(anime_names)
        most_used = counter.most_common(1)
        
        print("Returning the response: " + trending_topics)

        return MostUsedTopicsResponse(most_used[0][0]) if most_used else NotFound("No topics found")
    
    def TopicSubscribers(self, request, context):

        print("Processing a TopicSubscribers request")
        
        res = []

        for topic in self.Topics:
            if topic.name in request.topicnames:
                micro_service_response = []
                print("Received response from other micro service for topic name: " + topic_name)
                subscribers = topic.subscribers
                res.append(topsubscribers)
                
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

        print("Returning the response")

        return GetTopicsResponse(topics = self.Topics) #if len(topics > 0) else NotFound("No topics found")
    
    def CreateTopic(self, request, context):

        print("Processing a CreateTopic request")

        micro_service_response = 'topicname'
        print("Received response from other micro service")
        res = request.topicname

        self.Topics.append(Topic(topic_name = res, subscribers = [], publications = []))

        print("Returning the response: " + res)

        return CreateTopicResponse(topicname = res)
    
    def GetTopic(self, request, context):

        print("Processing a GetTopic request")

        topic_name = request.topicname

        micro_service_response = Topic()
        print("Received response from other micro service")
        topic = self.Topics.get(topic_name)

        print("Returning the response: " + topic)

        return GetTopicResponse(topic = topic)
    
    def PublishMessage(self, request, context):

        print("Processing a PublishMessage request")

        topic_name = request.topicname
        publication_name = request.publicationname
        message = request.message

        for topic in self.Topics:
            if topic.name == topic_name:
                micro_service_response = Topic()
                print("Received response from other micro service")
                topic.publications.append(
                    Publication(
                        name = publication_name,
                        topicname = topic_name,
                        content = Message(
                            username = message.username,
                            content = message.content,
                        )
                    )
                )
                 
        print("Returning the response: " + publication_name)

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
                        content = Image(
                            name = image.name,
                            username = image.username,
                        )
                    )
                )
                 
        print("Returning the response: " + publication_name)

        return PublishInTopicResponse(publicationname = publication_name)

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
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
