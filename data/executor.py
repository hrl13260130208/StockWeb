'''
    股票数据下载器
        executor：   根据下载任务，使用线程池下载数据

'''

import logging
from threading import Thread
from common.static import Static
from concurrent.futures import ThreadPoolExecutor


# ==========================
#   下载任务执行器
# ==========================
class DownloadExecutor(Thread):

    def __init__(self):
        self.logger = logging.getLogger("DownloadExecutor")
        super(DownloadExecutor, self).__init__()
        self.pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="download_")

    def run(self) -> None:
        self.logger.info("下载程序启动...")
        while (True):
            task = Static.DOWNLOAD_TASKS.get()
            self.logger.debug(f"获取到下载任务{task.name}。")
            self.pool.submit(task.start)


# ==========================
#   更新任务执行器
# ==========================
class UpdateExecutor(Thread):

    def __init__(self):
        self.logger = logging.getLogger("UpdateExecutor")
        super(UpdateExecutor, self).__init__()
        self.pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="update_")

    def run(self) -> None:
        self.logger.info("更新程序启动...")
        while (True):
            task = Static.UPDATE_TASKS.get()
            self.logger.debug(f"获取到更新任务{task}。")
            #   反射执行更新方法
            models = __import__(task["file"], fromlist=task["fromlist"])
            class_ = getattr(models, task["class"])
            if "class_args" in task.keys():
                obj = class_(*task["class_args"])
            else:
                obj = class_()

            func = getattr(obj, task["method"])
            if "method_args" in task.keys():
                self.pool.submit(func, *task["method_args"])
            else:
                self.pool.submit(func)
