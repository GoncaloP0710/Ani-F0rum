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
        
        response = self.stub.GetUserAchievements(ur_pb2.get_user_achievements_Request(user_name=request.user_name))
        achievements = response.achievements
        if achievements is None:
            return NotFound("User not found")


        return AchievementListResponse(achievements=achievements)
    
    def GetAchievement(self, request, context):
        response = self.stub.GetAchievement(ur_pb2.get_achievement_Request(title=request.title))
        achievement = response.achievement
        if achievement is None:
            return NotFound("achievement not found")
        
        return AchievementResponse(item=achievement)
    
    def UpdateAchievement(self, request, context):
        response = self.stub.UpdateUserAchievement(ur_pb2.update_user_achievement_Request(title=request.title, user_name=request.user_name))
        if response.success is None:
            return NotFound("achievement not found")
        
        return UpdateResponse(success=response.success)

        


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    add_AchievementsControllerServicer_to_server(
        achievements(), server
    )

   
    server.add_insecure_port("[::]:50080")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()