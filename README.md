# Ani-F-rum Project

## Authors

- André Reis - fc58192
- Daniel Nunes - fc58257
- Diogo Almeida - fc64854
- Gonçalo Pinto - fc58178

## Overview

Ani-F-rum is a cloud-based application designed to create an anime forum with a built-in social network. It provides REST and gRPC APIs for managing users, anime, topics, and recommendations. The project integrates multiple microservices to handle various functionalities such as user management, anime recommendations, topic discussions, and achievements.

---

## Architecture

The project is built using a microservices architecture, with each service responsible for a specific domain. Communication between services is achieved using gRPC, while REST APIs are exposed for external interaction.

---

## REST APIs

### User REST API
- **File**: [`python/controller/Users/swagger.yml`](python/controller/Users/swagger.yml)
- **Description**: Manages user-related operations such as creating users, retrieving user details, and managing achievements.
- **Endpoints**:
  - `/user`: Create a new user.
  - `/user/{user_name}/related_by_anime`: Get users related by anime preferences.
  - `/user/{user_name}/related_by_message`: Get users related by messages.
  - `/user/{user_name}/achievements`: Retrieve user achievements.
  - `/user/{user_name}/{achievement_name}`: Add an achievement to a user.
  - `/user/{user_name}/karma`: Retrieve user karma.
  - `/user/{user_name}/track_records`: Retrieve user track records.
  - `/user/{user_name}/messages`: Retrieve user messages.
  - `/user/{user_name}/recomended_animeList`: Get recommended anime for a user.

### Anime REST API
- **File**: [`python/controller/Anime/swagger.yml`](python/controller/Anime/swagger.yml)
- **Description**: Manages anime-related operations such as retrieving anime details and recommendations.
- **Endpoints**:
  - `/anime`: Retrieve a list of all anime.
  - `/anime/anime_name/{anime_name}`: Retrieve details of a specific anime.
  - `/anime/anime_name/{anime_name}/related`: Retrieve related anime.

---

## gRPC Services

### UserRecommendations Service
- **File**: [`protobufs/others/UserRecommendations.proto`](protobufs/others/UserRecommendations.proto)
- **Description**: Provides recommendations for users based on anime preferences, messages, and topics.
- **Methods**:
  - `GetUsersRelatedByAnime`: Retrieve users related by anime preferences.
  - `GetUsersRelatedByMessage`: Retrieve users related by messages.
  - `GetUsersRelatedByTopics`: Retrieve users related by topics.
  - `GetRecomendedAnimeListByTopics`: Retrieve recommended anime based on topics.

### AnimeList Service
- **File**: [`protobufs/others/AnimeList.proto`](protobufs/others/AnimeList.proto)
- **Description**: Handles anime data retrieval and recommendations.
- **Methods**:
  - `GetAllAnimes`: Retrieve all anime.
  - `GetAnimeByName`: Retrieve details of a specific anime.
  - `GetMultipleAnimeByName`: Retrieve details of multiple anime.
  - `GetSimilarAnime`: Retrieve similar anime.
  - `GetRecomendedAnimeList`: Retrieve recommended anime for a user.

### AnimeRepository Service
- **File**: [`protobufs/repository/AnimeRepository.proto`](protobufs/repository/AnimeRepository.proto)
- **Description**: Interacts with the database to fetch anime data.
- **Methods**:
  - `Animes`: Retrieve all anime.
  - `AnimeByName`: Retrieve details of a specific anime.
  - `MultipleAnimeByName`: Retrieve details of multiple anime.
  - `AnimeRelatedByGenre`: Retrieve anime by genre.

### UserRepository Service
- **File**: [`protobufs/repository/UserRepository.proto`](protobufs/repository/UserRepository.proto)
- **Description**: Interacts with the database to fetch user data.
- **Methods**:
  - `GetUser`: Retrieve details of a specific user.
  - `GetAllUsers`: Retrieve all users.
  - `GetUsersThatWatchedAnime`: Retrieve users who watched specific anime.
  - `UpdateUser`: Update user details.

---

## Common Protobuf Definitions

### Anime
- **File**: [`protobufs/Common/Anime.proto`](protobufs/Common/Anime.proto)
- **Description**: Defines the structure of an anime object.
- **Fields**:
  - `name`: Name of the anime.
  - `genres`: List of genres.
  - `episodes`: Number of episodes.
  - `score`: Rating score.
  - `aired`: Airing date.
  - `synopsis`: Synopsis of the anime.

### User
- **File**: [`protobufs/Common/User.proto`](protobufs/Common/User.proto)
- **Description**: Defines the structure of a user object.
- **Fields**:
  - `user_name`: Username.
  - `password`: Password.
  - `location`: User location.
  - `animes_watched`: List of watched anime.
  - `anime_watched_score`: Scores for watched anime.
  - `topics_subscribed`: Subscribed topics.
  - `karma`: User karma points.
  - `achievements`: List of achievements.

---

## Controllers

### User Controller
- **File**: [`python/controller/Users/user_controller.py`](python/controller/Users/user_controller.py)
- **Description**: Implements the logic for user-related REST endpoints.
- **Key Functions**:
  - `get_related_by_anime`: Retrieves users related by anime preferences.
  - `all_users`: Retrieves all users.
  - `get_user`: Retrieves details of a specific user.
  - `get_karma`: Retrieves user karma.
  - `top10Anime`: Retrieves the top 10 anime for a user.
  - `list_topics`: Retrieves the most used topics.

### Anime Controller
- **File**: [`python/controller/Anime/anime_controller.py`](python/controller/Anime/anime_controller.py)
- **Description**: Implements the logic for anime-related REST endpoints.
- **Key Functions**:
  - `all_anime`: Retrieves all anime.
  - `get_anime`: Retrieves details of a specific anime.
  - `get_similar_anime`: Retrieves similar anime.

---

## Dataset

The project uses the [MyAnimeList Dataset](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset) for anime-related data. The dataset includes titles, genres, ratings, and more.

---

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
```