# URL Shortener Take-Home Project
This project is a URL shortener service designed to create concise, memorable URLs from lengthy or complex ones. It’s built to handle high traffic with optimal performance by leveraging a modern tech stack.


## Features


* POST `/url/shorten`: accepts a URL to shorten (e.g. https://www.google.com) and returns a short URL that 
  can be resolved at a later time (e.g. http://localhost:8000/r/abc)
* GET `r/<short_url>`: resolve the given short URL (e.g. http://localhost:8000/r/abc) to its original URL
  (e.g. https://www.google.com). If the short URL is unknown, an HTTP 404 response is returned.
* DELETE `url/<short_url>`: deletes the given short URL if exist (e.g. http://localhost:8000/url/abc)
* POST `/url/custom-shorten`: accepts a URL and customer short URL to our service (e.g. https://www.google.com, google) and generates it if is available to use

## Architecture
This project uses a layered architecture, ensuring separation of concerns and ease of maintenance. See the detailed architectural flow in the diagram included below.
![URL Shortener Architecture](https://github.com/geeta-kukreja/url_shortener/blob/7cf2432d5256dbde51dcb7fa444d741e162b437a/diagram.jpeg)

## Installation

### Prerequisites
- Python 3.8+
- Docker
- MongoDB
- Redis

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/geeta-kukreja/url-shortener.git

## Getting Started


### Running the service

To run the web service in interactive mode, use the following command:
```commandline
pip install -r requirements.txt
```
```commandline
docker-compose up -d

```
```commandline
uvicorn app.main:app --reload

```

By default, the web service will run on port 8000.