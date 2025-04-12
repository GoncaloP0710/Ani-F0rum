import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import random
from concurrent import futures

import grpc
from python.others.FeedGenerator.FeedGenerator_pb2_grpc import(
    FeedGeneratorServiceStub,
    FeedGeneratorServiceServicer,
    add_FeedGeneratorServiceServicer_to_server
)
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from python.others.FeedGenerator.FeedGenerator_pb2 import (
    FeedResponse,
    TopicFeedResponse,
)
from python.repository.User.UserRepository_pb2_grpc import (
    UserRepositoryStub
)
from python.Common.User_pb2 import (
    Rarity,
    Achievement,
    User
)

from python.Common.Topic_pb2 import (
    Subscriber,
    Message,
    Image,
    Publication,
    Topic,
)

from python.repository.User import UserRepository_pb2_grpc as ur_grpc
from python.repository.User import UserRepository_pb2 as ur_pb2
from python.repository.Topic import TopicRepository_pb2_grpc
from python.repository.Topic import TopicRepository_pb2

class FeedGenerator(FeedGeneratorServiceServicer):

    def __init__(self):
        self.user_channel = grpc.insecure_channel('localhost:50043')  # Create a channel to the UserRepository
        self.user_stub = UserRepositoryStub(self.user_channel)

        self.topic_channel = grpc.insecure_channel('localhost:50062')  # Create a channel to the TopicRepository
        self.topic_stub = TopicRepository_pb2_grpc.TopicRepositoryStub(self.topic_channel)

    #all publications from all topics subscribed
    def GetFeed(self, request, context):
        
        response = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        user = response.user
        if user is None:
            return NotFound("User not found")
        
        print("user found: ", user.user_name)

        feed = []
        for topic_name in user.topics_subscribed:
            
            response_topic = self.topic_stub.GetTopic(TopicRepository_pb2.GetTopicRequest(topicname=topic_name))
            topic = response_topic.topic
            if not topic:
                context.abort(grpc.StatusCode.NOT_FOUND, "Topic not found")
            
            print("topic found: ", topic.topicname)

            feed.extend(topic.publications)
                
        return FeedResponse(feed=feed)

    #all topics subscribed
    def GetTopicFeed(self, request, context):

        response = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        user = response.user
        if user is None:
            return NotFound("User not found")
        
        feed = []
        for topic_name in user.topics_subscribed:
            
            response_topic = self.topic_stub.GetTopic(TopicRepository_pb2.GetTopicRequest(topicname=topic_name))
            topic = response_topic.topic
            if not topic:
                context.abort(grpc.StatusCode.NOT_FOUND, "Topic not found")

            feed.append(topic)

        return TopicFeedResponse(topic_feed=feed)

#TODO
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_FeedGeneratorServiceServicer_to_server(
        FeedGenerator(), server
    )

    server.add_insecure_port("[::]:50094")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()