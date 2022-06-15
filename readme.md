# Google Rate Tester

The purpose of this repo is to test how waiting between requests to google search affects how many requests can be made before google starts rate limiting (returning a http status code 429) while using the python package `googlesearch-python`

## Hypothesis

My hypnosis is that no rate limit will cause there to be fewer successful requests before receiving a 429, but a delays longer then 5 seconds will yield little to no difference.

## Method

The file main.py utilizes `googlesearch-python` to make a series of automated requests to google based on the configuration values set in `config.json`.

In this test the parameters set where `"delay_tests": [0, 1, 2, 4, 5, 15, 30]` and `"samples_per_test": 14`. This means the test is repeated 14 times for a delay of 0.15, 1, 2, 4, 5, 15, and 30 seconds.

In the config file, the `Proxies` value was filled in with proxies obtained from https://proxy.webshare.io. All proxies where located within the usa and where purchased under the cheapest available plan. All ip addresses where datacenter ip's.

Multithreading was used in order to ensure requests where sent at the exact right delay, that way the speed of the proxies and of `googlesearch-python` would have less of an effect on the test results. Requests are continuously sent with the time delay between them regardless of if the last request has resolved or not with a limit of up to 10 unresolved requests at once (important for testing 0-second delays). Once a single request resolves with http 429, new requests are no longer sent and the program waits until all unresolved requests resolve and tally's the amount of 200 response codes with at least one result. For each search a random search term is selected from `search_items`.