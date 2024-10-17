# JioSaavn Flask App

This Flask application provides a simple API interface for fetching songs, albums, and playlists from [JioSaavn](https://www.jiosaavn.com/) using the [JioSaavnAPI](https://cyberboysumanjay.github.io/JioSaavnAPI/).

## Features
- 🎵 **Fetch song details** by name or ID.
- 📀 **Retrieve album and playlist data.**
- 🚀 **Lightweight Dockerized Flask app.**

## Tech Stack
- **Flask**: Python micro web framework.
- **JioSaavnAPI**: An unofficial API to interact with JioSaavn.
- **Docker**: Containerized deployment.

## Installation and Usage

### 1. Clone the Repository
git clone https://github.com/vasanti1705/jiosavan-app.git
cd jiosavan-app

### 2. Prerequisites
Before you begin, ensure that you have **Docker** installed on your machine. You can download it from the official [Docker website](https://www.docker.com/get-started).

### 3. Running the App Locally

Follow these simple steps to get your app up and running:

1. **Pull the Docker image from DockerHub:**
   
   docker pull vasanti1705/jiosaavn-flask

2. **Run the Docker container:**

   docker run -p 5100:5100 vasanti1705/jiosaavn-flask

🎉 **Your app should now be running at http://localhost:5100!** 🎉

**PREVIEW**
![image](https://github.com/user-attachments/assets/60b0ebf3-e645-48ae-b1df-2260c4b4e837)

