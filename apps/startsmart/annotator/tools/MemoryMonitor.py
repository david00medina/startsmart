from threading import Thread
from statistics import mean
import nvidia_smi
import time


class MemoryMonitor(Thread):
    def __init__(self, delay):
        super(MemoryMonitor, self).__init__()
        self.__stopped = False
        self.__delay = delay

        nvidia_smi.nvmlInit()
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)
        self.__info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
        self.__used_memory = [self.__info.used / (1024**2)]
        self.__total_memory = self.__info.total / (1024**2)

        self.start()

    @property
    def used_memory(self):
        return mean(self.__used_memory)

    def run(self) -> None:
        while not self.__stopped:
            self.__used_memory.append(self.__info.used / (1024**2))
            time.sleep(self.__delay)

    def stop(self):
        self.__stopped = True
        nvidia_smi.nvmlShutdown()