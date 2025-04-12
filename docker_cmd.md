# Anime Network

docker network create anime-network

# Anime Repository

docker build -t anime-repository -f python/repository/Anime/Dockerfile .

docker run --rm -d --name anime-repository --network anime-network -p 50053:50053 anime-repository

# Anime List 

docker build -t anime-list -f python/others/AnimeList/Dockerfile .

docker run --rm -it --name anime-list --network anime-network -p 50052:50052 anime-list

# Anime Controller 

docker build -t anime-controller -f python/controller/Anime/Dockerfile .

docker run --rm -it --name anime-controller --network anime-network -p 50051:50051 anime-controller

# Anime Client 

docker build -t anime-client -f python/Tests/AnimeRelated/Dockerfile .

docker run --rm -it --name anime-client --network anime-network anime-client

# User Network 

docker network create user-network

# User Repository 

docker build -t user-repository -f python/repository/User/Dockerfile .

docker run --rm -d --name user-repository --network user-network -p 50043:50043 user-repository

# User Recommendations 

docker build -t user-recommendations -f python/others/UserRecommendations/Dockerfile .

docker run --rm -it --name user-recommendations --network user-network -p 50042:50042 user-recommendations

# User Controller

docker build -t user-controller -f python/controller/Users/Dockerfile .

docker run --rm -it --name user-controller --network user-network -p 50040:50040 user-controller

docker network connect anime-network user-controller

# User Client

docker build -t user-client -f python/Tests/UserRelated/Dockerfile .

docker run --rm -it --name user-client --network user-network user-client
