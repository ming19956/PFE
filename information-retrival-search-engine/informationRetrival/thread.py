from threading import Thread  # 创建线程的模块
import os
class MyThread(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):  # 固定名字run ！！！必须用固定名
        os.system("bert-serving-start -model_dir /Users/liujiazhen/Documents/2020-2021/PFE/PFE/uncased_L-12_H-768_A-12 -num_worker=1 -port 8190 -port_out 8191")