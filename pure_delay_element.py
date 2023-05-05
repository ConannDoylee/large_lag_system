import numpy as np
import yaml
import os
import threading
import time
from matplotlib import pyplot as plt
from base_element import BaseElement
ROOT = os.path.abspath(os.path.dirname(__file__))

class PureDelayElement(BaseElement):
    def __init__(self):
        self.name = 'PureDelayElement'
        self.conf_file = ROOT + "/conf/pure_delay_element.yaml"
        super(PureDelayElement, self).__init__(self.name,file=self.conf_file)
        # params
        self.T_delay = self.model_conf['T_delay']
        self.N = max(int(self.T_delay // self.T_step),1)
        self.input = [[self.name,self.model_conf['init_input']]]
        self.output = [[self.name,self.model_conf['init_output']]]
        self.buffer = [0]*self.N

        return

    def run_once(self):
        input = self.input[0][1]
        if len(self.buffer) == self.N:
            output = self.buffer.pop()
            self.output = [[self.name,output]]
            self.buffer.insert(0,input)
        else:
            self.buffer.append(input)
        return

    def test(self):
        input_list = []
        output_list = []
        time_list = []
        self.thread_start()
        time_start = time.time()
        for u in np.arange(60):
            time_now = time.time()
            self.update_input(u)
            output = self.get_output()
            time_list.append(time_now-time_start)
            input_list.append(u)
            output_list.append(output)
            time.sleep(0.01)
        plt.plot(time_list,input_list)
        plt.plot(time_list,output_list)
        self.stop_thread()
        plt.show()
        return
    
def main():
    pure_delay = PureDelayElement('.')
    pure_delay.test()

# if __name__ == '__main__':
#     main()