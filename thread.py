import pyautogui
import threading
from time import perf_counter, sleep
from queue import Queue


def recognize(uiResource, confidence, timeout, waitTime):
    result = None
    print(f'Looking for: {uiResource}')
    start = perf_counter()
    while perf_counter()-start < timeout:
        print(f'Looking with confidence lvl: {confidence}')
        result = pyautogui.locateOnScreen(uiResource, confidence)
        if result:
            print(f'Found image {uiResource} in {result}')
            break
        sleep(waitTime)
    else:
        print('Timeout')
        return result
    return result


# print(recognize('notfound.png', 0.9, 10, 1))
# print(recognize('icon1.png', 0.9, 10, 1))


def locateByThread(imagesList, confidence, timeout, waitTime):
    que = Queue()
    threads = [threading.Thread(target=lambda q, img, conf, time, wait: q.put(recognize(img, conf, time, wait)), args=(que, image, confidence, timeout, waitTime)) for image in imagesList]
    for thread in threads:
        thread.daemon = True
        thread.start()
    return que.get()


start = perf_counter()
wynik = locateByThread(['notfound.png', 'icon2.png', 'icon3.png', 'icon1.png'], 0.9, 10, 1)
print(perf_counter()- start)
if wynik:
    print(wynik)
    pyautogui.moveTo(wynik[0], wynik[1])
