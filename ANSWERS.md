# Docker Compose Lab — Answers

Name:

Fill this in as you go. For every **Prediction**, write your answer down
*before* you run anything. You are not graded on whether your prediction was
right — you are graded on having made one and explained the gap.

---

## Stage 1 — Run the broken stack

**Prediction 1.** You are about to `docker compose up` a stack where `api`
depends on `db` with a plain `depends_on`. Will the api start successfully?
Why or why not?

> 

**What actually happened** (paste the relevant lines from the api logs):

> 

**Q1.** `docker compose ps` shows the `db` container as running. The api still
could not reach it. What is the difference between those two statements?

> 

---

## Stage 2 — Make the api wait for readiness

**Q2.** You added a healthcheck and changed `depends_on` to use
`condition: service_healthy`. In your own words, what is `pg_isready` actually
testing, and why can't Compose figure that out on its own?

> 

**Q3.** A classmate says "just put a retry loop in the api, then you don't need
any of this." Give one argument for their approach and one against it.

> 

---

## Stage 3 — Add migrations

**Q4.** `flyway` uses `condition: service_completed_successfully` while `db`
uses `condition: service_healthy`. Why do those two services need different
conditions?

> 

**Q5.** Run `docker compose ps -a` after the stack is up. What state is the
flyway container in, and is that a problem?

> 

---

## Stage 4 — Talk to the second service

**Prediction 2.** `ML_SERVICE_URL` is currently `http://localhost:8080`, and
the `ml` service does publish port 8080. From inside the `api` container, will
that URL reach the ml service?

> 

**What actually happened:**

> 

**Q6.** Explain what `localhost` means from inside a container, and why
`http://ml:8080` works when `http://localhost:8080` does not.

> 

**Q7.** `ml` publishes `8080:8080`, so you can reach it from your own browser
at `localhost:8080`. Does the `api` service need that published port in order
to call it? Try removing the `ports:` block from `ml` and find out.

> 

---

## Stage 5 — Where the data lives

Add a player through the api so there is something in the database to lose.

**Prediction 3.** With no `volumes:` on the `db` service, will your new player
still be there after `docker compose down` and `docker compose up`?

> 

**What actually happened:**

> 

Now add the named volume.

**Prediction 4.** With the named volume in place, will the player survive
`docker compose down` and come back up?

> 

**Prediction 5.** Will it survive `docker compose down -v`?

> 

**What actually happened for both:**

> 

**Q8.** The `api` service has `./app:/app` and the `db` service now has
`postgres-data:/var/lib/postgresql/data`. Both are under `volumes:`. What is
the difference between them, and why does `api` want one kind and `db` the
other?

> 

---

## Wrap-up

**Q9.** Which of your five predictions were wrong? Pick the one that surprised
you most and explain what you had misunderstood.

> 

**Q10.** The stack you just built is a description of a deployment
architecture. Name one quality attribute from this course that a Compose file
helps you achieve, and point at the specific lines in your
`docker-compose.yaml` that do it.

> 
