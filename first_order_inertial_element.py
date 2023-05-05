import numpy as np
from matplotlib import pyplot as plt
import copy
import yaml
import os
import threading
import time
from base_element import BaseElement
ROOT = os.path.abspath(os.path.dirname(__file__))

class FirstOrderInertialElement(BaseElement):
    def __init__(self):
        self.name = 'FirstOrderInertialElement'
        self.conf_file = ROOT  + "/conf/first_order_inertial_element.yaml"
        super(FirstOrderInertialElement, self).__init__(self.name,file=self.conf_file)
        # params
        self.N = self.model_conf['N']
        self.k = self.model_conf['k']
        self.tau = self.model_conf['tau']
        self.input = [[self.name,self.model_conf['init_input']]]
        self.X = self.model_conf['init_output']
        return

    def f(self,X_k):
        input = self.input[0][1]
        # f = dx = AX + Bu
        A = -1 / self.tau
        B = self.k / self.tau
        f = A * X_k + B * input
        return f
    
    def odeRK4(self):
        dt = self.T_step / self.N
        for i in np.arange(self.N):
            K1 = self.f(self.X)
            K2 = self.f(self.X+K1*dt/2)
            K3 = self.f(self.X+K2*dt/2)
            K4 = self.f(self.X+K3*dt)
            self.X += dt/6.0*(K1+2.0*K2+2.0*K3+K4)
        return

    def run_once(self):
        self.odeRK4()
        self.output = [[self.name,copy.copy(self.X)]]
        return

    def test(self):
        input_list = []
        output_list = []
        time_list = []
        self.thread_start()
        time_start = time.time()
        for i in np.arange(600):
            u = 1
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
        plt.grid()
        plt.show()
        return
    
def main():
    model = FirstOrderInertialElement('.')
    model.test()

# if __name__ == '__main__':
    # main()