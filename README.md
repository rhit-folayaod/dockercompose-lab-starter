# Docker Compose Lab

A small four-service web application for you to take apart and put back
together. It predicts how many points an NBA player will score against a given
opponent.

| Service  | What it is                                               |
|----------|----------------------------------------------------------|
| `db`     | PostgreSQL 16                                             |
| `flyway` | Runs the SQL migrations in `sql/`, then exits             |
| `ml`     | A tiny prediction service the api calls over the network  |
| `api`    | FastAPI app on port 8000, talks to both `db` and `ml`     |

The application code is not the point of this lab and you should not need to
change it. Everything you edit lives in `docker-compose.yaml`.

**The `docker-compose.yaml` in this repo is broken on purpose.** Getting it
working is the lab.

## Before you start

You need Docker Desktop running. Verify with:

```
docker compose version
```

Then create your environment file:

```
cp .env.example .env
```

Compose reads `.env` automatically to fill in the `${POSTGRES_...}` values. If
you skip this step, those values resolve to empty strings and you will get
confusing failures that have nothing to do with the actual lab.

## Working through the stages

Each stage builds on the one before it. If you get stuck and want to move on,
every stage has a known-good starting point on its own branch:

```
git checkout stage-3-start
```

That gets you a working stack as of the end of the previous stage, so one bad
stage never costs you the rest of the lab. Commit your own work on a branch of
your own first so you do not lose it.

## Useful commands

```
docker compose up              # start, and keep logs in the foreground
docker compose up -d           # start in the background
docker compose ps              # what is running, and whether it is healthy
docker compose logs api        # logs for one service
docker compose down            # stop and remove containers
docker compose down -v         # ...and remove named volumes too
```

## Turning it in

Record your answers in `ANSWERS.md` as you go. Write each prediction down
**before** you run the command — a prediction you make after seeing the result
is not a prediction.
