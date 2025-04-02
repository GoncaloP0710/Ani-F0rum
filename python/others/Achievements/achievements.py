import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

import random
from concurrent import futures

import grpc
from python.others.Achievements.Achievements_pb2_grpc import(
    AchievementsControllerServicer,
    AchievementsControllerStub,
    add_AchievementsControllerServicer_to_server
)
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from python.others.Achievements.Achievements_pb2 import (
    AchievementListResponse,
    AchievementResponse,
    UpdateResponse,
)
from python.repository.User.UserRepository_pb2_grpc import (
    UserRepositoryStub
)

from python.repository.User import UserRepository_pb2_grpc as ur_grpc
from python.repository.User import UserRepository_pb2 as ur_pb2

class achievements(AchievementsControllerServicer):

    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50043')  # Create a channel to the UserRepository
        self.stub = UserRepositoryStub(self.channel)

    def GetAchivementList(self, request, context):
        
        user = self.stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if user is None:
            return NotFound("User not found")

        # micro_service_response = []
        # achievementList = [Achievement(n) for n in micro_service_response] # interagir com o próximo microserviço

        return AchievementListResponse(user.achievements)
    
    def GetAchievement(self, request, context):

        user = self.stub.GetUser(ur_pb2.get_user_Request(user_name=request.user_name))
        if user is None:
            return NotFound("User not found")
        
        for achievement in user.achievements:
            if achievement.title == request.title:
                return AchievementResponse(achievement)
            
        return NotFound("Achievement not found")
    
    def UpdateAchievement(self, request, context):
        user2up = request.user_to_update
        ach = request.new
        user = self.stub.GetUser(ur_pb2.get_user_Request(user_name=user2up.user_name))
        if user is None:
            return NotFound("User not found")
        
        for achievement in user.achievements:
            if achievement.title == ach.title:
                user.achievements.pop(achievement)
                user.achievements.append(ach)
                return UpdateResponse(self.stub.UpdateUser(ur_pb2.get_user_Request(user=user)))

        


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AchievementsControllerServicer_to_server(
        achievements(), server
    )

   
    server.add_insecure_port("[::]:443")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()