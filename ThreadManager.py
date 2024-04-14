import os
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()
# class ThreadManager:
#     def __init__(self, workers=os.cpu_count() + 4):
#         self.workers = workers
#
#     def get_executor(self):
#         executor = ThreadPoolExecutor(max_workers=self.workers)
#         return executor
#     pass
