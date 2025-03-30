import random
from concurrent import futures

import grpc
import FeedGenerator_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from FeedGenerator_pb2 import (
    FeedRequest,
    FeedResponse,
    TopicFeedRequest,
    TopicFeedResponse,
)

from python.repository.User import UserRepository_pb2_grpc as ur_grpc
from python.repository.User import UserRepository_pb2 as ur_pb2

class FeedGenerator(FeedGenerator_pb2_grpc.AchievementsServicer):

    def __init__(self):
        self.user_channel = grpc.insecure_channel('localhost:50054')  # Create a channel to the UserRepository
        self.user_stub = FeedGenerator_pb2_grpc.FeedGeneratorService(self.user_channel)


    def GetFeed(self, request, context):
        
        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if user is None:
            return NotFound("User not found")
        
        feed = []
        for topic in user.topics_subscribed:
            feed.extend(topic.publications)
        return FeedResponse(feed)

    def GetTopicFeed(self, request, context):

        user = self.user_stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if user is None:
            return NotFound("User not found")
        return TopicFeedResponse(user.topics_subscribed)

#TODO
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    FeedGenerator_pb2_grpc.add_FeedGeneratorServicer_to_server(
        FeedGenerator(), server
    )

    server.add_insecure_port("[::]:50061")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()