# Docker Compose - Spike starter

A small four-service application for you to take apart and put back together.
It predicts how many points an NBA player will score against a given opponent.

| Service  | What it is                                               |
|----------|----------------------------------------------------------|
| `db`     | PostgreSQL 16                                             |
| `flyway` | Runs the SQL migrations in `sql/`, then exits             |
| `ml`     | A small prediction service the api calls over the network |
| `api`    | Web API on port 8000, talks to both `db` and `ml`         |

The application code is not the point of this Spike and you should not need to
change it. Everything you edit lives in `docker-compose.yaml`.

**The `docker-compose.yaml` in this repo is broken on purpose.** Getting it
working is the Spike.

Do the Lab first. You are supposed to arrive here with a map already drawn and
some predictions already written down.

## Setup

**1. Start Docker Desktop**, then confirm the daemon is actually running:

```
docker info
```

Installing Docker and running Docker are different things, and the error you
get when it is not running does not tell you to start it.

**2. Make your branch.** Name it with your Rose-Hulman username:

```
git checkout -b yourusername
```

**3. Create your environment file:**

```
cp .env.example .env
```

Compose reads `.env` automatically to fill in the `${POSTGRES_...}` values.
Skip this and they resolve to empty strings, and you will get confusing
failures that have nothing to do with the Spike.

> Copy `.env.example` as-is - don't change the values in it. `flyway.conf`
> has the same database name, user and password written into it separately, so
> changing one and not the other breaks the migrations in a way that looks like
> a totally unrelated problem.

**4. Bring it up and watch it fail:**

```
docker compose up
```

## If you get stuck on a stage

Each stage builds on the one before it. If one defeats you and you want to keep
going, you can pull in a known-good compose file for the next stage without
losing any of your own work:

```
git checkout stage-3-start -- docker-compose.yaml
```

That replaces only `docker-compose.yaml` and leaves everything else on your
branch alone. Commit your own attempt first so you still have it.

## Useful commands

```
docker compose up              # start, logs in the foreground
docker compose up -d           # start in the background
docker compose ps              # what is running, and whether it is healthy
docker compose ps -a           # ...including containers that have exited
docker compose logs api        # logs for one service
docker compose down            # stop and remove containers
docker compose down -v         # ...and remove named volumes too
```

## Turning it in

Fill in `ANSWERS.md` as you go. Write each prediction **before** you run the
command - a prediction made after you have seen the result is not a prediction,
and it is obvious in the writing.

Your Spike deliverable is a PDF. See the handout for what goes in it.
