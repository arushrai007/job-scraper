## 1. Why this ingestion strategy?

I chose a source-adapter based ingestion pipeline using the public
Arbeitnow Job Board API for the live demonstration rather than
directly targeting protected platforms such as LinkedIn.

The pipeline separates fetching, validation, storage, and the web
layer. Job data is fetched using Python `requests`, validated against
the expected job structure, deduplicated, and stored locally before
being exposed through a small Flask web application so i could not get same data every time and resulting in garbage collection.

I chose this approach because it demonstrates the complete ingestion
flow while keeping the live demo within the assignment's low-risk
source requirement. It also makes the source-specific part of the
system replaceable if the source changes or becomes unavailable i checked even by breaking the urls it handled gracefully with rollback atleast 3 times.

The system uses request timeouts, controlled pacing, retries with
increasing backoff, response validation, and graceful failure rather
than repeatedly hitting a failing source. I deliberately did not
attempt to bypass CAPTCHA, authentication, or other access controls.
If the primary source became unavailable, I would stop retrying after
a bounded number of attempts and switch to another permitted source
adapter rather than attempting to circumvent the restriction.

## 2. Trade off

I prioritized a reliable end-to-end ingestion pipeline over building
a complex frontend or integrating multiple job platforms because of my techstack and my previous experince while building this type of project.

The current implementation demonstrates fetching, validation,
deduplication, storage, error handling, retry/backoff, and a deployed
Flask interface using one source.
With a full week, I would add additional permitted source adapters,
stronger source-health monitoring, more comprehensive automated
tests, and a more polished frontend. I would also improve persistent
storage and observability for production-scale usage.
One practical trade-off was using Render's free tier for deployment.
It is sufficient for the demonstration but can spin down when idle,
so the first request after inactivity may take longer.


## 3. Use of AI tools

I used AI tools throughout development to understand statements, terms, generate initial code, to design and for test cases and asked for frontend design building.

I personally ran and tested the code rather than submitting
unverified generated output implemented my own logic. During testing, I intentionally broke
the source URL to verify retry and graceful-failure behavior u can find those in commits even i tried to change the formatting or syntax we could say for arbit now add it handled that too well didnt collapsed.

One useful issue discovered during testing was that an invalid source
could return a response that was not valid JSON. The original error
handling only caught `requests` exceptions, so the JSON parsing error
was not handled correctly. I verified the failure, identified the
difference between the exception types, and broadened the handling to
cover malformed JSON as well.

All final implementation logics and behavior's were tested locally
before deployment by myself.
