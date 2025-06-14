# Ani-F-rum Project

## Authors

- [André Reis](https://github.com/4Sparkz) - fc58192
- [Daniel Nunes](https://github.com/DanunesL) - fc58257
- [Diogo Almeida](https://github.com/wartuga) - fc64854
- [Gonçalo Pinto](https://github.com/GoncaloP0710) - fc58178

---

## Overview

Ani-F-rum is a cloud-based application designed to create an anime forum with a built-in social network. It provides REST and gRPC APIs for managing users, anime, topics, and recommendations. The project integrates multiple microservices to handle various functionalities such as user management, anime recommendations, topic discussions, and achievements.

### Dataset

The project uses the [MyAnimeList Dataset](https://www.kaggle.com/datasets/dbdmobile/myanimelist-dataset) for anime-related data. The dataset includes titles, genres, ratings, and more.

---

## Architecture

The project is built using a microservices architecture, with each service responsible for a specific domain. Communication between services is achieved using gRPC, while REST APIs are exposed for external interaction.

<img src="draw.png" alt="plot" width="500"/>

### Kubernetes

Each micro-service recives per minute an http requests to check on their status and has a `deployment_service.yml` and a `scaler.yml`

#### Deployment_service
- configure resource utilization through requests and limits
- probes for liveness, readiness, and start-up

#### Scaler
- autoscaling through HPA

### Entry Point

It would be implemented using a HTTP(s) ingress or Kubernetes Gateway but due to time restrictions we were not able to finish it.

### Controllers

Controllers are responsible for implementing the logic behind the REST API endpoints. They act as intermediaries between the client requests and the underlying services or repositories. For example:
- The **Anime Controller** (`anime_controller.py`) handles anime-related operations such as retrieving anime details and fetching similar anime.
- Controllers often use gRPC services to fetch data or perform operations, ensuring a clean separation of concerns.

### Others

The "Others" section refers to additional services or utilities that support the main functionality of the application. These include:
- **AnimeList Service**: Handles anime-related data retrieval and recommendations. It interacts with the `AnimeRepository` to fetch data from the database.
- These services are implemented using gRPC and are defined in their respective `.proto` files.

### Repository

Repositories are responsible for interacting with the database. They provide low-level data access methods that are used by the gRPC services. For example:
- **AnimeRepository**: Fetches anime data from the database, such as anime details, genres, and related anime.

---

## Tests Preview

<div align="center">
  <img src="/README_Files/anime_controller_pod.png" alt="plot" width="500"/>
  <p><em>Figure: Anime controller pod test Results</em></p>
</div>

<div align="center">
  <img src="/README_Files/anime-list-hpa.png" alt="plot" width="500"/>
  <p><em>Figure: Anime list hpa test Results</em></p>
</div>

## How to run

(outdated) [All the information needed is here](cmd_promps/cummernets.md).

(new) chmod +x deploy.sh (for premissions)
./deploy.sh (This may take a while, only works on fc58192 google cloud account)

## Close cluster

gcloud container clusters delete ani-cluster --region=europe-west1
