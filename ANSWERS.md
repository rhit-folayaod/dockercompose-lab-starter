# Spike Worksheet

Name: Ethan Schurr

Fill this in as you work through the stages. Every **Prediction** gets written
down *before* you run anything.

You are not graded on whether a prediction was right. You are graded on having
made one and being able to explain the gap.

This file is your Spike deliverable. Commit it on your branch and push it
when you are done.

---

## Stage 1 — Why did it fail?

**What happened** (paste the lines from the api where it gives up):

> api-1  | startup check FAILED: cannot reach the database -- connection to server at "db" (172.21.0.2), port 5432 failed: Connection refused
> api-1  |        Is the server running on that host and accepting TCP/IP connections?
> api-1  | 
> api-1 exited with code 1

**Q1.** `docker compose ps` reports the `db` container as running, and the api
still could not reach it. What is the difference between those two statements?

>  The issue is that the db was not yet ready to connect to the API.
> The difference comes in the fact that teh API should wait for a health check then connect. Time is the problem

**Q2.** Look back at the map you drew in the Lab. Did you predict this failure?
If you predicted a different symptom, what did you expect instead?

> Yes, I expected this.

---

## Stage 2 — Make the api wait for readiness

**Q3.** You added a healthcheck and changed how `depends_on` works. In your own
words, what is `pg_isready` actually testing, and why can Compose not work that
out by itself?

> Yup. Basically asks if Postgres is ready to accept connections
> Compose should not have logic for each db implementation. So this pg_isready script tests this and tells us it db is ready.

**Q4.** A classmate says "just put a retry loop in the api and you don't need
any of this." Give one argument for their approach and one against it.

> For: That would be easy for the API to use
> Against: It would need to be implemented everywhere instead once in the docker compose script.

---

## Stage 3 — Add the migration job

**Q5.** `flyway` needs a different `depends_on` condition than `db` does. Why?
What is different about a job that is supposed to finish?

> Flyway needs to make sure that the API knows its ready with the DBs data.
> Additionally, the DB must be ready for Flyway to actually put data in it.

**Q6.** Run `docker compose ps -a` once the stack is up. What state is the
flyway container in? Is that a problem?

> Flyway exited (0), this just means that it finished its job and no longer is running. No issues.

---

## Stage 4 — Let the services talk

**PREDICTION 1.** `ML_SERVICE_URL` is `http://localhost:8080`, and the `ml`
service publishes port 8080. From inside the `api` container, will that URL
reach the ml service?

> The program will not work since localhost does not actually leave the NIC of container

**What actually happened:**

> The program crashed for the earlier reason.

**Q7.** Explain what `localhost` means from inside a container, and why
`http://ml:8080` works when `http://localhost:8080` does not.

> inside a container localhost is the loopback connection to itself. So it will not send data out of the container.
> ml:8080 sends data out of the container to the dns server which then converts it to an ip that the docker container can route with.

**Q8.** You can reach the ml service from your own browser at
`localhost:8080` because it publishes that port. Does the `api` need that
published port in order to call it? Remove the `ports:` block from `ml` and
find out.

> Each docker container can reach each other on their little network regardless if we designate ports.
> However, if we do not publish ports then I cannot reach them from my pc browser.

---

## Stage 5 — Where the data lives

Add a player through the api first, so there is something to lose.

**PREDICTION 2.** With no `volumes:` on `db`, will your player still be there
after `docker compose down` and `docker compose up`?

> No. That data is not stored anywhere that is permanent because it is only stored in the writable layer of the container which will be lost when the container is brought back.

**PREDICTION 3.** With a named volume, will it survive `docker compose down`?

> Yes. The volumes will persist.

**PREDICTION 4.** With a named volume, will it survive `docker compose down -v`?

> No, we are killing the volumes with that command.

**What actually happened, for all three:**

> What I said prior.

**Q9.** `api` has `./app:/app` and `db` has
`postgres-data:/var/lib/postgresql/data`. Both sit under `volumes:`. What is
the difference between them, and why does each service want the kind it has?

> the api is mounted to my computer so my pc manages that.
> postgres however is in the volumes which is managed by Docker.

---

## Timing

How long did a full `docker compose down -v` followed by `docker compose up`
take, from nothing to the api answering a request?

> 4.7 to 10.88

How does that compare against the success measure you set for yourself in the
Lab?

> My measure was 3 commands to bring up the system. Now it only takes 1-2 commands. So it did great.

---

## Analyze

**Q10.** Look at everything you changed. How much of it was application code,
and how much was configuration?

> It was all configs through compose

**Q11.** Did your approach introduce any new problems? Anything that is now
slower, more complicated, or easier to get wrong?

> Not that I am aware of. This should make the management of scripts and instructions much easier.

**Q12.** What does someone have to know about this compose file that they would
not have had to know about the twelve-step README?

> How Docker compose works. The evil README can cry about it. All in all, this is simplier once Docker is set up.

---

## Reflect

**R1.** Did your implementation hit the success measure you set for yourself in
the Lab? If you missed it, by how much, and what would close the gap?

> Yes.

**R2.** Go back to the failures you predicted in step 3 of the Lab. Which ones
happened the way you described? Which showed up as a completely different
symptom than you expected?

> Mine were pretty on point.

**R3.** Which of your predictions during the Spike were wrong? Pick the one that
surprised you most and explain what you had misunderstood.

> Not really any. I have used compose prior.

**R4.** In the Lab you listed what a configuration file would need to be able to
express. Compare that against what you actually wrote. What did you miss, and
what turned out to be unnecessary?

> My psydo code was probably too simplistic so I was missing some details. Mainly some checks to make sure everything was ready like I needed in my graphical picture.

**Optional.** Name one thing about this stack that would still stop you from
running it anywhere other than your own laptop.

> WSL2 lol. (Though now that I think about it, they did recently release a way to run it natively on Windows.)
