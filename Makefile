run:
    docker-compose up --build

test:
    pytest

clean:
    docker-compose down
    docker system prune -f
# run-local:
#     uvicorn server:app --host 0.0.0.0 --port 5000 --reload
