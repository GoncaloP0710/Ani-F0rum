import random
from concurrent import futures

import grpc
import achievements_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from achievements_pb2 import (
    Achievement,
    User,
    AchievementListRequest,
    AchievementListResponse,
    AchievementRequest,
    AchievementResponse,
    UpdateRequest,
    UpdateResponse,
)

class Achievements(achievements_pb2_grpc.AchievementsServicer):
    def GetAchivementList(self, request, context):

        micro_service_response = []
        achievementList = [Achievement(n) for n in micro_service_response] # interagir com o próximo microserviço

        return AchievementListResponse(achievementList)
    
    def GetAchievement(self, request, context):

        name = request.name

        micro_service_response = Achievement()
        achievement = micro_service_response

        return AchievementResponse(achievement)
    
    def UpdateAchievement(self, request, context):
        ...


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )
    achievements_pb2_grpc.add_AchievementsServicer_to_server(
        RecommendationService(), server
    )

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
    server.add_secure_port("[::]:443", creds)
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()