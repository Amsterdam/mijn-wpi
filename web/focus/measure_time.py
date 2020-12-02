import time


class MeasureTime:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        self._start_time = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()

        print("Elapsed", self.name, end - self._start_time)
