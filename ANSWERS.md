# Spike Worksheet

Name:

Fill this in as you work through the stages. Every **Prediction** gets written
down *before* you run anything.

You are not graded on whether a prediction was right. You are graded on having
made one and being able to explain the gap.

This file is your Spike deliverable. Commit it on your branch and push it
when you are done.

---

## Stage 1 — Why did it fail?

**What happened** (paste the lines from the api where it gives up):

> 

**Q1.** `docker compose ps` reports the `db` container as running, and the api
still could not reach it. What is the difference between those two statements?

> 

**Q2.** Look back at the map you drew in the Lab. Did you predict this failure?
If you predicted a different symptom, what did you expect instead?

> 

---

## Stage 2 — Make the api wait for readiness

**Q3.** You added a healthcheck and changed how `depends_on` works. In your own
words, what is `pg_isready` actually testing, and why can Compose not work that
out by itself?

> 

**Q4.** A classmate says "just put a retry loop in the api and you don't need
any of this." Give one argument for their approach and one against it.

> 

---

## Stage 3 — Add the migration job

**Q5.** `flyway` needs a different `depends_on` condition than `db` does. Why?
What is different about a job that is supposed to finish?

> 

**Q6.** Run `docker compose ps -a` once the stack is up. What state is the
flyway container in? Is that a problem?

> 

---

## Stage 4 — Let the services talk

**PREDICTION 1.** `ML_SERVICE_URL` is `http://localhost:8080`, and the `ml`
service publishes port 8080. From inside the `api` container, will that URL
reach the ml service?

> 

**What actually happened:**

> 

**Q7.** Explain what `localhost` means from inside a container, and why
`http://ml:8080` works when `http://localhost:8080` does not.

> 

**Q8.** You can reach the ml service from your own browser at
`localhost:8080` because it publishes that port. Does the `api` need that
published port in order to call it? Remove the `ports:` block from `ml` and
find out.

> 

---

## Stage 5 — Where the data lives

Add a player through the api first, so there is something to lose.

**PREDICTION 2.** With no `volumes:` on `db`, will your player still be there
after `docker compose down` and `docker compose up`?

> 

**PREDICTION 3.** With a named volume, will it survive `docker compose down`?

> 

**PREDICTION 4.** With a named volume, will it survive `docker compose down -v`?

> 

**What actually happened, for all three:**

> 

**Q9.** `api` has `./app:/app` and `db` has
`postgres-data:/var/lib/postgresql/data`. Both sit under `volumes:`. What is
the difference between them, and why does each service want the kind it has?

> 

---

## Timing

How long did a full `docker compose down -v` followed by `docker compose up`
take, from nothing to the api answering a request?

> 

How does that compare against the success measure you set for yourself in the
Lab?

> 

---

## Analyze

**Q10.** Look at everything you changed. How much of it was application code,
and how much was configuration?

> 

**Q11.** Did your approach introduce any new problems? Anything that is now
slower, more complicated, or easier to get wrong?

> 

**Q12.** What does someone have to know about this compose file that they would
not have had to know about the twelve-step README?

> 

---

## Reflect

**R1.** Did your implementation hit the success measure you set for yourself in
the Lab? If you missed it, by how much, and what would close the gap?

> 

**R2.** Go back to the failures you predicted in step 3 of the Lab. Which ones
happened the way you described? Which showed up as a completely different
symptom than you expected?

> 

**R3.** Which of your predictions during the Spike were wrong? Pick the one that
surprised you most and explain what you had misunderstood.

> 

**R4.** In the Lab you listed what a configuration file would need to be able to
express. Compare that against what you actually wrote. What did you miss, and
what turned out to be unnecessary?

> 

**Optional.** Name one thing about this stack that would still stop you from
running it anywhere other than your own laptop.

>
