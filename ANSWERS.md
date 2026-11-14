# Spike Worksheet

Name: Remi Schwartz

Fill this in as you work through the stages. Every **Prediction** gets written
down *before* you run anything.

You are not graded on whether a prediction was right. You are graded on having
made one and being able to explain the gap.

This file is your Spike deliverable. Commit it on your branch and push it
when you are done.

---

## Stage 1 — Why did it fail?

**What happened** (paste the lines from the api where it gives up):

> api-1 | startup check FAILED: cannot reach the database -- 
> connection to server at "db" (172.19.0.2), port 5432 failed: Connection refused
> api-1 | Is the server running on that host and accepting TCP/IP connections?
> api-1 exited with code 1

**Q1.** `docker compose ps` reports the `db` container as running, and the api
still could not reach it. What is the difference between those two statements?

> Running means the container's process has started, but it does not mean PostgreSQL is ready to accept connections. The database was still initializing when the API tried to connect, which caused the connection refused error.

**Q2.** Look back at the map you drew in the Lab. Did you predict this failure?
If you predicted a different symptom, what did you expect instead?

> Yes, I predicted that database connection problems could cause the API to fail or crash. This happened when the API tried to connect before PostgreSQL was ready. The API received a connection refused error and exited with code 1. The specific issue was that Docker Compose started the database container without waiting for PostgreSQL to accept connections.

---

## Stage 2 — Make the api wait for readiness

**Q3.** You added a healthcheck and changed how `depends_on` works. In your own
words, what is `pg_isready` actually testing, and why can Compose not work that
out by itself?

> pg_isready checks whether PostgreSQL is accepting connections. Docker Compose can tell when a container starts, but it cannot automatically know when the database inside is ready. The healthcheck gives Compose a way to verify readiness before starting the API.


**Q4.** A classmate says "just put a retry loop in the api and you don't need
any of this." Give one argument for their approach and one against it.

> A retry loop could help the API recover if the database temporarily becomes unavailable, even after startup. However, it would require adding logic to the application code. Using a healthcheck keeps the startup dependency in the Compose configuration and prevents the API from starting before the database is ready.

---

## Stage 3 — Add the migration job

**Q5.** `flyway` needs a different `depends_on` condition than `db` does. Why?
What is different about a job that is supposed to finish?

> PostgreSQL is a service that needs to stay running, so we wait for it to become healthy. Flyway is different because it runs the migrations and then exits. The API needs to wait for Flyway to finish successfully, which is why I used service_completed_successfully.

**Q6.** Run `docker compose ps -a` once the stack is up. What state is the
flyway container in? Is that a problem?

> Flyway was in the exited state after completing its migrations successfully. This is not a problem because Flyway is a one-time job rather than a service that needs to keep running. An exit code of 0 means it finished successfully.

---

## Stage 4 — Let the services talk

**PREDICTION 1.** `ML_SERVICE_URL` is `http://localhost:8080`, and the `ml`
service publishes port 8080. From inside the `api` container, will that URL
reach the ml service?

> I predicted that it would work because the ML service was publishing port 8080.

**What actually happened:**

> The prediction request failed with a connection refused error. After changing the URL to http://ml:8080, the API successfully connected to the ML service and created a prediction.

**Q7.** Explain what `localhost` means from inside a container, and why
`http://ml:8080` works when `http://localhost:8080` does not.

> Inside a container, localhost refers to that specific container, not my computer or another container. Since ML runs in a separate container, the API cannot reach it using localhost. Docker Compose provides internal networking that allows containers to communicate using service names, so http://ml:8080 works.


**Q8.** You can reach the ml service from your own browser at
`localhost:8080` because it publishes that port. Does the `api` need that
published port in order to call it? Remove the `ports:` block from `ml` and
find out.

> No, the API does not need the ML service's port published to the host. I removed the ML ports: block and used http://ml:8080 for communication. The prediction request succeeded, confirming that the containers could communicate through Docker's internal network without exposing the ML port to my computer.

---

## Stage 5 — Where the data lives

Add a player through the api first, so there is something to lose.

**PREDICTION 2.** With no `volumes:` on `db`, will your player still be there
after `docker compose down` and `docker compose up`?

> I predicted that the player would disappear because the database container would be removed and recreated.

**PREDICTION 3.** With a named volume, will it survive `docker compose down`?

> I predicted that the player would survive because the named volume stores data separately from the container.

**PREDICTION 4.** With a named volume, will it survive `docker compose down -v`?

> I predicted that the player would disappear because the -v flag removes the named volume.

**What actually happened, for all three:**

> Without a named volume, I restarted the stack and saw only the three original players. However, my attempt to add a test player before that restart had not succeeded, so that test did not conclusively prove data loss.

> After adding the named volume, I successfully created Test Player with ID 4. I ran docker compose down and restarted everything, and Test Player was still there.

> Then I ran docker compose down -v and restarted the stack. Test Player disappeared, leaving only Jayson Tatum, LeBron James, and Shai Gilgeous-Alexander. This confirmed that the named volume preserved data during a normal shutdown but was deleted when I used -v.

**Q9.** `api` has `./app:/app` and `db` has
`postgres-data:/var/lib/postgresql/data`. Both sit under `volumes:`. What is
the difference between them, and why does each service want the kind it has?

> ./app:/app is a bind mount that connects my local application folder to the API container. This is useful during development because the container can access my local code. postgres-data:/var/lib/postgresql/data is a Docker-managed named volume that stores the database files separately from the container. The API needs access to the project files, while PostgreSQL needs persistent storage so its data is not lost when the container is recreated.

---

## Timing

How long did a full `docker compose down -v` followed by `docker compose up`
take, from nothing to the api answering a request?

> I measured 12.6033395 seconds (about 12.60 seconds) for docker compose up --build -d after running docker compose down -v. The first /teams request failed because the connection closed unexpectedly, but the second request succeeded and returned all three teams. The exact time until the API answered successfully was not measured.

How does that compare against the success measure you set for yourself in the
Lab?

> My success measure was to start the complete stack using one command in under five minutes. The Compose startup command completed in 12.60 seconds, which was well under the five-minute target. The API also responded successfully when I retried the request, although I did not measure the full time to that successful response.

---

## Analyze

**Q10.** Look at everything you changed. How much of it was application code,
and how much was configuration?

> Almost everything I changed was configuration in docker-compose.yaml. I added a healthcheck, changed the startup dependencies, added Flyway and ML services, fixed the ML service URL, and configured a named volume. I did not need to change the application code to solve these problems.

**Q11.** Did your approach introduce any new problems? Anything that is now
slower, more complicated, or easier to get wrong?

> The Compose file became more complicated as I added services, dependencies, and volumes. I ran into several YAML indentation and formatting errors that prevented Docker Compose from starting. The healthchecks and migrations also add some startup time because the API has to wait for the other services. However, this makes startup more reliable.

**Q12.** What does someone have to know about this compose file that they would
not have had to know about the twelve-step README?

> Someone using the Compose file needs to understand YAML formatting, service names, healthchecks, dependency conditions, and volumes. They also need to understand that containers communicate through Docker's internal network instead of localhost. However, they no longer need to manually remember the order of all the startup commands because Compose handles those dependencies.

---

## Reflect

**R1.** Did your implementation hit the success measure you set for yourself in
the Lab? If you missed it, by how much, and what would close the gap?

> My implementation met the one-command startup goal and completed the Compose startup in 12.60 seconds, well under five minutes. I also verified that the database, migrations, API, and ML service worked. One thing I would improve is adding an API healthcheck because the first request immediately after startup failed. That would make it easier to tell when the entire application is ready.

**R2.** Go back to the failures you predicted in step 3 of the Lab. Which ones
happened the way you described? Which showed up as a completely different
symptom than you expected?

> I predicted problems with database readiness, migrations, ML connections, and database availability. The database readiness problem happened when the API crashed because PostgreSQL was not ready. The ML connection problem also happened when the API tried to reach the ML service using localhost. The migration problem did not happen after I configured Flyway correctly because the API waited for migrations to finish successfully. Most of the failures appeared as connection errors, which matched what I expected.

**R3.** Which of your predictions during the Spike were wrong? Pick the one that
surprised you most and explain what you had misunderstood.

> My prediction about localhost was wrong. I expected the API to reach the ML service because port 8080 was published. Instead, the connection failed. I misunderstood that localhost inside a container refers to that container itself. I learned that each container has its own localhost and that containers should use Docker Compose service names to communicate with each other.

**R4.** In the Lab you listed what a configuration file would need to be able to
express. Compare that against what you actually wrote. What did you miss, and
what turned out to be unnecessary?

> In my Lab, I identified that the configuration needed to define services, dependencies, healthchecks, networking, environment variables, volumes, and ports. I ended up using all of these in my Compose file. What I had not fully considered was the difference between waiting for a service to become healthy and waiting for a one-time job to finish successfully. I also learned that publishing the ML port was unnecessary because the API could communicate with ML through Docker's internal network.

**Optional.** Name one thing about this stack that would still stop you from
running it anywhere other than your own laptop.

>
