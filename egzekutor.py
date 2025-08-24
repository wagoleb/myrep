import pyautogui
import threading
from time import perf_counter, sleep
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed


def recognize(uiResource, confidence, timeout, waitTime):
    result = None
    print(f"Looking for: {confidence}")
    start = perf_counter()
    while perf_counter() - start < timeout:
        # print(f'Looking with confidence lvl: {confidence}')
        result = pyautogui.locateOnScreen(uiResource, confidence)
        if result:
            print(f"Found image {confidence}")
            break
        sleep(waitTime)
    else:
        print(f"Timeout {confidence}")
        return result
    return result


def multipleConfidence(uiResource, timeout, waitTime):
    confLevels = [x / 100 for x in range(100, 80 - 1, -5)]
    with ThreadPoolExecutor(max_workers=len(confLevels)) as executor:
        workers = [(lvl, executor.submit(recognize, uiResource, lvl, timeout, waitTime)) for lvl in confLevels]
        result_list = [(worker[0], worker[1].result()) for worker in workers]
        print(max(result_list)[1])


start = perf_counter()
# print(recognize('notfound.png', confidence = 1, timeout = 2, waitTime = 1))
multipleConfidence("search.png", 3, 1)
print(round(perf_counter() - start, 3))
