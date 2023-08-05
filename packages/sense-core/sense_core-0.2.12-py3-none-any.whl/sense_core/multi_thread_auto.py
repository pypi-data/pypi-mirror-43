import multiprocessing
import time
from sense_core import RabbitmqFactory


class ThreadAutoFactory(object):
    def __init__(self, queue, label, threshold=100, work=3, max_work=10, monitor=60):
        """
        :param queue:      消费队列
        :param label:      消费的mq
        :param auto_large: 伸缩最大阈值，当msg_num > work * auto_large 则work数加1
        :param auto_small: 伸缩最小阈值，当msg_num < work * auto_small 则work数减1
        :param work:       初始work数，也即最小work数
        :param max_work:   最大work数
        :param monitor:    监控间隔时间，每多少时间进行一次work和msg检查，进行auto scale
        """
        self.queue = queue
        self.threshold = threshold
        self.work = work
        self.max_work = max_work
        self.min_work = work
        self.mq = RabbitmqFactory(label)
        self.thread_list = []
        self.monitor = monitor
        self.msg_num = self.get_mq_queue_num()

    def get_mq_queue_num(self):
        _code, queue_details = self.mq.list_queues(dict_type=True)
        return queue_details.get(self.queue, 0)

    def auto_scale_num(self):
        # 获取队列长度，并进行work数变更
        self.msg_num = self.get_mq_queue_num()
        if self.msg_num > self.threshold * len(self.thread_list):
            self.work += 1
            if self.work > self.max_work:
                self.work = self.max_work
        else:
            self.work -= 1
            if self.work < self.min_work:
                self.work = self.min_work
        return self.work

    def execute(self, function, params=()):
        while True:
            # work 扩张
            if self.work > len(self.thread_list):
                _append = self.work - len(self.thread_list)
                for num in range(0, _append):
                    self.thread_list.append(multiprocessing.Process(target=function, args=params))
                for thread in self.thread_list:
                    if not thread.is_alive():
                        thread.start()
            time.sleep(self.monitor)
            self.work = self.auto_scale_num()
            # work 缩减
            if self.work < len(self.thread_list):
                _del_num = len(self.thread_list) - self.work
                for thread in self.thread_list[:_del_num]:
                    thread.terminate()
                    thread.join()
                    self.thread_list.remove(thread)