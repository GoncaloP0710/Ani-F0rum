import random
from concurrent import futures

import grpc
import achievements_pb2_grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from achievements_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
)

class RecommendationService(achievements_pb2_grpc.AchievementsServicer):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            raise NotFound("Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(books_for_category, num_results)

        return RecommendationResponse(achievements=books_to_recommend)


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