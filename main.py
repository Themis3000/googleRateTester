from googlesearch import search
from concurrent.futures import ThreadPoolExecutor
import time
import random
import json

with open("config.json", "r") as f:
    config = json.load(f)


results = {}
got_non_ok = False


def proxies_gen():
    for proxy in config["proxies"]:
        yield {"https": proxy}


def random_term():
    return random.choice(config["search_items"])


def make_request(proxy, label, sub_label):
    start = time.time()
    term = random_term()
    try:
        print(f"looking up {term} and recording under {label} with proxy {proxy}")
        if random.random() < .4:
            raise Exception("Request failed")
        time.sleep(random.random()*4)
    except:
        global got_non_ok
        got_non_ok = True
        print("Got error, concluding sample")
        return
    time_taken = time.time() - start
    results[label][sub_label].append({"term": term, "time_taken": time_taken})
    print(f"done - looked up {term} in {time_taken} secs")


proxies = proxies_gen()

for test_delay in config["delay_tests"]:
    print(f"---Starting test for {test_delay} sec delay---")
    results[test_delay] = []
    for test_num in range(config["samples_per_test"]):
        print(f"Starting sample #{test_num+1}")
        results[test_delay].append([])
        proxy = next(proxies)
        executor = ThreadPoolExecutor(max_workers=config["max_concurrency"])
        while not got_non_ok:
            executor.submit(make_request, proxy, test_delay, test_num)
            time.sleep(test_delay)
        executor.shutdown(wait=True, cancel_futures=True)
        got_non_ok = False


with open("results.json", "w") as f:
    json.dump(results, f)
