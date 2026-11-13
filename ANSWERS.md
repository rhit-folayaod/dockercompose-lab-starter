# Spike Worksheet

Name: Jasmeen Kaur

Fill this in as you work through the stages. Every **Prediction** gets written
down *before* you run anything.

You are not graded on whether a prediction was right. You are graded on having
made one and being able to explain the gap.

This file is your Spike deliverable. Commit it on your branch and push it
when you are done.

---

## Stage 1 — Why did it fail?

**What happened** (paste the lines from the api where it gives up):
> api-1  | startup check FAILED: cannot reach the database -- connection to server at "db" (172.20.0.2), port 5432 failed: Connection refused api-1  |  Is the server running on that host and accepting TCP/IP connections? api-1  | 

**Q1.** `docker compose ps` reports the `db` container as running, and the api
still could not reach it. What is the difference between those two statements?

> The database container was running but the database was still not ready to accept connections yet

**Q2.** Look back at the map you drew in the Lab. Did you predict this failure?
If you predicted a different symptom, what did you expect instead?

> Yes I predicted this failure because I wrote that the API might start before PostgreSQL is ready and show a database connection error

---

## Stage 2 — Make the api wait for readiness

**Q3.** You added a healthcheck and changed how `depends_on` works. In your own
words, what is `pg_isready` actually testing, and why can Compose not work that
out by itself?

> pg_isready checks if the database is ready to accept connections and Compose can't tell this because it only checks if the container is running

**Q4.** A classmate says "just put a retry loop in the api and you don't need
any of this." Give one argument for their approach and one against it.

> A retry loop allows the API to keep trying to connect if the database takes longer to start but it will make the application more complicated because you have to write and maintain extra code

---

## Stage 3 — Add the migration job

**Q5.** `flyway` needs a different `depends_on` condition than `db` does. Why?
What is different about a job that is supposed to finish?

> Flyway uses a different condition because it runs the migrations and then stops while the database needs to stay running so the API can use it

**Q6.** Run `docker compose ps -a` once the stack is up. What state is the
flyway container in? Is that a problem?

> Flyway shows Exited (0) and this is not a problem because it means the migrations finished successfully

---

## Stage 4 — Let the services talk

**PREDICTION 1.** `ML_SERVICE_URL` is `http://localhost:8080`, and the `ml`
service publishes port 8080. From inside the `api` container, will that URL
reach the ml service?

> Yes

**What actually happened:**

> localhost:8080 did not reach the ML service because it pointed to the API container

**Q7.** Explain what `localhost` means from inside a container, and why
`http://ml:8080` works when `http://localhost:8080` does not.

> localhost means the container you are currently inside and http://ml:8080 works because Docker uses the service name ml to connect the API to the ML container

**Q8.** You can reach the ml service from your own browser at
`localhost:8080` because it publishes that port. Does the `api` need that
published port in order to call it? Remove the `ports:` block from `ml` and
find out.

> No because it can connect to ML through Docker internal network with ml:8080
---

## Stage 5 — Where the data lives

Add a player through the api first, so there is something to lose.

**PREDICTION 2.** With no `volumes:` on `db`, will your player still be there
after `docker compose down` and `docker compose up`?

> No I think that the player will be gone because the data is not saved in a volume

**PREDICTION 3.** With a named volume, will it survive `docker compose down`?

> Yes I think that the player should still be there because the named volume keeps the database data even when the container is removed

**PREDICTION 4.** With a named volume, will it survive `docker compose down -v`?

> NO the player will be lost because -v removes the named volume (I actually did this once during my internship without realizing what -v does and let me just say that it did not end well)

**What actually happened, for all three:**

> with no volume: The player was lost after docker compose down and docker compose up
> with named volume: The player was still there after docker compose down and docker compose up
> with named volume with down -v: The player was lost because the volume was deleted

**Q9.** `api` has `./app:/app` and `db` has
`postgres-data:/var/lib/postgresql/data`. Both sit under `volumes:`. What is
the difference between them, and why does each service want the kind it has?

> ./app:/app lets the API use the files from my computer and postgres-data saves the database information so it doesn't get lost when the container is removed

---

## Timing

How long did a full `docker compose down -v` followed by `docker compose up`
take, from nothing to the api answering a request?

> It took about 1 minute and 9 seconds to start everything and get the API responding

How does that compare against the success measure you set for yourself in the
Lab?

> My goal was to get the entire application running in under 5 minutes and I met my goal because it took less than 5 minutes

---

## Analyze

**Q10.** Look at everything you changed. How much of it was application code,
and how much was configuration?

> All of my changes were in the docker-compose.yml and I did not have to chaneg any of the code

**Q11.** Did your approach introduce any new problems? Anything that is now
slower, more complicated, or easier to get wrong?

> Yes there are more services and settings to manage which makes the configuration a little more complicated. I don't think startup takes much longer and in my opinion I think it is still faster and easier than starting everything separately without Docker Compose.

**Q12.** What does someone have to know about this compose file that they would
not have had to know about the twelve-step README?

> Someone needs to know how the services work together, how they connect/depend on each other, and how the volumes work.

---

## Reflect

**R1.** Did your implementation hit the success measure you set for yourself in
the Lab? If you missed it, by how much, and what would close the gap?

> Yes I met my goal. My goal was to get the whole application running in under 5 minutes and it took about 1 minute and 9 seconds

**R2.** Go back to the failures you predicted in step 3 of the Lab. Which ones
happened the way you described? Which showed up as a completely different
symptom than you expected?

> I correctly predicted that the API could fail if the database was not ready and I also predicted that Flyway could fail if it started before the database was ready

**R3.** Which of your predictions during the Spike were wrong? Pick the one that
surprised you most and explain what you had misunderstood.

> My prediction about localhost:8080 was wrong because I thought it would connect to ML but I learned that localhost only connects to the container itself and I needed to use ml:8080 to connect to the ML service.

**R4.** In the Lab you listed what a configuration file would need to be able to
express. Compare that against what you actually wrote. What did you miss, and
what turned out to be unnecessary?

> I missed the volumes. I also thought I needed to publish the ML port but it was not necessary because the API could connect to ML directly through Docker.

**Optional.** Name one thing about this stack that would still stop you from
running it anywhere other than your own laptop.

> The .env file