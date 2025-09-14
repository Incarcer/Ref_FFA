# Yahoo Fantasy Football Analyst (Refactored)

This repository contains the refactored source code for the Yahoo Fantasy Football Analyst application. It has been restructured to create a secure, scalable, and maintainable foundation using a modern technology stack.

## Architecture Overview

The application follows a containerized, service-oriented architecture, composed of three main services orchestrated by Docker Compose:

1.  **`postgres`**: A PostgreSQL database service for persistent data storage. It stores all user data, league information, rosters, and player stats.
2.  **`backend`**: A Python backend built with **FastAPI**. It handles all business logic, secure authentication with the Yahoo API, and serves a RESTful API for the frontend.
3.  **`frontend`**: A modern single-page application built with **React** and **Vite**. It provides the user interface and communicates with the backend via HTTP and WebSockets.

This separation of concerns ensures that the application is modular, scalable, and easier to develop and maintain.

## Tech Stack

-   **Backend**: Python, FastAPI, SQLAlchemy, Pydantic
-   **Frontend**: React, Vite, Tailwind CSS
-   **Database**: PostgreSQL
-   **Containerization**: Docker, Docker Compose

## Getting Started

Follow these instructions to get the development environment up and running on your local machine.

### Prerequisites

-   [Docker](https://www.docker.com/get-started/) and [Docker Compose](https://docs.docker.com/compose/install/) must be installed.
-   You need a Yahoo Developer App to get a Client ID and Secret. You can create one on the [Yahoo Developer Network](https://developer.yahoo.com/apps/create/).

### 1. Environment Configuration

The backend requires a set of environment variables to connect to the database and the Yahoo API.

1.  Navigate to the `backend/` directory.
2.  Create a `.env` file by copying the template:
    ```bash
    cp .env.template .env
