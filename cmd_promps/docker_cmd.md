# Anime Network

```python
docker network create anime-network
```

# Anime Repository

```python
docker build -t anime-repository -f python/repository/Anime/Dockerfile .
```

```python
docker run --rm -d --name anime-repository --network anime-network -p 50053:50053 anime-repository
```
# Anime List 

```python
docker build -t anime-list -f python/others/AnimeList/Dockerfile .
```

```python
docker run --rm -it --name anime-list --network anime-network -p 50052:50052 anime-list
```

# Anime Controller 

```python
docker build -t anime-controller -f python/controller/Anime/Dockerfile .
```

```python
docker run --rm -it --name anime-controller --network anime-network -p 50051:50051 anime-controller
```

# Anime Client 

```python
docker build -t anime-client -f python/Tests/AnimeRelated/Dockerfile .
```

```python
docker run --rm -it --name anime-client --network anime-network anime-client
```

# User Network 

```python
docker network create user-network
```

# User Repository 

```python
docker build -t user-repository -f python/repository/User/Dockerfile .
```

```python
docker run --rm -d --name user-repository --network user-network -p 50043:50043 user-repository
```

# User Recommendations 

```python
docker build -t user-recommendations -f python/others/UserRecommendations/Dockerfile .
```

```python
docker run --rm -it --name user-recommendations --network user-network -p 50042:50042 user-recommendations
```

# User Statistics

```python
docker build -t user-statistics -f python/others/UserStatistics/Dockerfile .
```

```python
docker run --rm -it --name user-statistics --network user-network -p 50041:50041 user-statistics
```

```python
docker network connect anime-network user-statistics
```

# User Controller

```python
docker build -t user-controller -f python/controller/Users/Dockerfile .
```

```python
docker run --rm -it --name user-controller --network user-network -p 50040:50040 user-controller
```

```python
docker network connect anime-network user-controller
```


# Feed Generator 

```python
docker build -t feed-generator -f python/others/FeedGenerator/Dockerfile .
```

```python
docker run --rm -it --name feed-generator --network user-network -p 50094:50094 feed-generator
```


# Achievements

```python
docker build -t achievements -f python/others/Achievements/Dockerfile .
```

```python
docker run --rm -it --name achievements --network user-network -p 50080:50080 achievements
```


# User Client

```python
docker build -t user-client -f python/Tests/UserRelated/Dockerfile .
```

```python
docker run --rm -it --name user-client --network user-network user-client
```

# Topics Network

```python
docker network create topics-network
```

# Topics Repository

```python
docker build -t topic-repository -f python/repository/Topic/Dockerfile .
```

```python
docker run --rm -d --name topic-repository --network topics-network -p 50062:50062 topic-repository
```
# Topics List 

```python
docker build -t publisher -f python/others/Publisher/Dockerfile .
```

```python
docker run --rm -it --name publisher --network topics-network -p 50061:50061 publisher
```

# Topics Controller 

```python
docker build -t topics-controller -f python/controller/Topics/Dockerfile .
```

```python
docker run --rm -it --name topics-controller --network topics-network -p 50060:50060 topics-controller
```

# Topics Client 

```python
docker build -t topics-client -f python/Tests/TopicRelated/Dockerfile .
```

```python
docker run --rm -it --name topics-client --network topics-network topics-client
```