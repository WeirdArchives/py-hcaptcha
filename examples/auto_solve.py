# For this, you'll need to have redis set up:
# https://redislabs.com/blog/redis-on-windows-10/

# You'll also need a list of HTTP proxies in the file `proxies.txt`

import threading
import multiprocessing
import win32process
import itertools
import hcaptcha
import xrequests

WORKER_COUNT = 16
THREAD_COUNT_PER_WORKER = 50
SOLVER_PARAMS = dict(
    min_answers=3
)
CHALLENGE_PARAMS = dict(
    sitekey="13257c82-e129-4f09-a733-2a7cb3102832",
    page_url="https://dashboard.hcaptcha.com/signup"
)
DROP_ON_SOLVE = True

def do_stuff_with_token(token, http_client, proxy):
    print(f"Obtained token: {token[:20]} ..")

def thread_func(worker_num, thread_num, thread_barrier, thread_event,
                proxies, solver):
    # initialize thread

    # wait for other threads and workers
    thread_barrier.wait()
    thread_event.wait()

    # run solver
    while True:
        proxy = next(proxies)
        http_client = xrequests.Session(proxies={
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }, timeout=5)

        while True:
            try:
                token = solver.get_token(
                    **CHALLENGE_PARAMS,
                    http_client=http_client)

                if token:
                    do_stuff_with_token(token, http_client, proxy)
                    if DROP_ON_SOLVE:
                        break

            except xrequests.exceptions.RequestException:
                break
            except hcaptcha.ApiError:
                break
            except Exception as err:
                print(F"Solver error: {err!r}")
                break

def worker_func(worker_num, worker_barrier, proxies):
    # calculate cpu core based on worker number
    cpu_num = worker_num % multiprocessing.cpu_count()
    # set cpu core to be used for this process
    win32process.SetProcessAffinityMask(-1, 1 << cpu_num)
    
    # create threads
    proxies = itertools.cycle(proxies)
    solver = hcaptcha.Solver(**SOLVER_PARAMS)
    thread_barrier = threading.Barrier(THREAD_COUNT_PER_WORKER + 1)
    thread_event = threading.Event()
    threads = [
        threading.Thread(
            target=thread_func,
            args=(worker_num, thread_num, thread_barrier, thread_event,
                  proxies, solver)
        )
        for thread_num in range(THREAD_COUNT_PER_WORKER)
    ]

    # start threads
    for thread in threads:
        thread.start()
    # wait until all threads are initialized
    thread_barrier.wait()
    # wait until all workers are initialized
    worker_barrier.wait()
    # run threads
    thread_event.set()
    
if __name__ == "__main__":
    # load proxies
    with open("proxies.txt") as fp:
        proxies = fp.read().splitlines()
        proxies_per = int(len(proxies)/WORKER_COUNT)
    
    # create workers
    worker_barrier = multiprocessing.Barrier(WORKER_COUNT + 1)
    workers = [
        multiprocessing.Process(
            target=worker_func,
            args=(worker_num, worker_barrier,
                  proxies[proxies_per * worker_num : proxies_per * (worker_num + 1)]
                 )
        )
        for worker_num in range(WORKER_COUNT)
    ]

    # start workers
    for worker in workers:
        worker.start()
    # wait until all threads are initialized
    worker_barrier.wait()