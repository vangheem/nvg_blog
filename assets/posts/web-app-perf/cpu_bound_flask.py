from flask import Flask
import time


DURATION = 0.5

app = Flask(__name__)


@app.route('/')
def cpu_bound():
    start = time.time()
    while True:
        9 * 9
        if (time.time() - start) > DURATION:
            break
    return 'done'
