import numpy as np
from matplotlib import pyplot as plt
import os
from base_element import BaseElement
import copy
ROOT = os.path.abspath(os.path.dirname(__file__))

class SmithCompensator(BaseElement):
    def __init__(self):
        self.name = 'smith'
        self.conf_file = ROOT + "/conf/smith_compensator.yaml"
        super(SmithCompensator, self).__init__(self.name,file=self.conf_file)
        self.N = self.model_conf['N']
        self.tau = self.model_conf['tau']
        self.input = [[self.name,self.model_conf['init_input']]]
        self.X = self.model_conf['init_output']
        self.T_delay = self.model_conf['T_delay']
        self.k = self.model_conf['k']
        self.buffer_size = max(int(self.T_delay/self.T_step),1)
        self.buffer = [0]*self.buffer_size
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
        if not self.model_conf['is_open']:
            self.output = [[self.name,0]]
            return
        # first order
        self.odeRK4()
        tmp_out = copy.copy(self.X)
        # pure delay
        if len(self.buffer) == self.buffer_size:
            output = self.buffer.pop()
            self.output = [[self.name,tmp_out-output]]
            self.buffer.insert(0,tmp_out)
        else:
            self.buffer.append(tmp_out)
        return
    
    def test(self):

        return

def main(root):
    smith = SmithCompensator()
    smith.test()
    plt.show()

if __name__ == '__main__':
    main(".")