import time

startTime_for_tic = 0
startTime_for_toc = 0


def tic():
    global startTime_for_tic
    global startTime_for_toc
    startTime_for_tic = startTime_for_toc = time.perf_counter_ns()


def toc(text: str = ""):
    global startTime_for_tic
    global startTime_for_toc
    newTime = time.perf_counter_ns()
    if 'startTime_for_tic' in globals():
        print("Elapsed time is % 12.3fms (tic) % 12.3fms (toc) %s" % (
            (newTime - startTime_for_tic) / 1000000,
            (newTime - startTime_for_toc) / 1000000,
            text
        ))
    else:
        print("Toc: start time not set")
    startTime_for_toc = newTime
