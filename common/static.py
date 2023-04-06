

import queue

class Static():
    #   下载任务队列
    DOWNLOAD_TASKS = queue.Queue(20000)
    #   更新任务队列
    UPDATE_TASKS = queue.Queue(20000)








