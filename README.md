## Run postgres locally
Make sure you have postgres running somewhere, an easy way to run it is with docker.
```
docker run -d -p 5432:5432 -e POSTGRES_USER=postgres -e \
POSTGRES_PASSWORD=postgres se POSTGRES_DB=tcg --name pgdb postgres
```

## To prepare everything after a fresh clone
```
cp .env.example .env  # Update env vars in .env
poetry install
poetry shell
alembic upgrade head
```

## To run server
```
poetry shell  # If not already in a shell
uvicorn app.main:app --reload
```

## To run tests
```
poetry shell  # If not already in a shell
scripts/test
```

## To run auto formatter
```
poetry shell # If not already in a shell
scripts/format
```