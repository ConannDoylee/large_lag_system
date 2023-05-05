from pure_delay_element import PureDelayElement
from first_order_inertial_element import FirstOrderInertialElement
from pid_controller import PID
from command import Command
from smith_compensator import SmithCompensator
from matplotlib import pyplot as plt
import time
import numpy as np

modules_dict = {
                "pure_delay":PureDelayElement(),
                "first_order":FirstOrderInertialElement(),
                "PID":PID(),
                "command":Command(),
                "smith": SmithCompensator()
                }

# "current_module": ["deps_input_module",""]
modules_inputs_deps = {
    "pure_delay": ["PID"],
    "first_order": ["pure_delay"],
    "PID": ["first_order","smith","command"],
    "smith": ["PID"]
}

modules_plot = ["PID","pure_delay","first_order","smith"]

class Simulation(object):
    def __init__(self):
        return

    def run_once(self):
        for module in modules_inputs_deps:
            outputs = []
            for input_module in modules_inputs_deps[module]:
                output = modules_dict[input_module].get_output()
                if output is not None:
                    outputs.extend(output)
            if output:
                modules_dict[module].update_input(outputs)

        return
    
    def start_modules(self):
        print("start_modules...")
        for key in modules_dict:
            print(key)
            modules_dict[key].thread_start()
        return

    def stop_modules(self):
        print("stop_modules...")
        for key in modules_dict:
            print(key)
            modules_dict[key].stop_thread()
        return
    
    def simulate(self,count,T_s=0.01):
        self.start_modules()
        for i in np.arange(count):
            self.run_once()
            time.sleep(T_s)
        self.stop_modules()
        return

    def plot_modules(self):
        for module in modules_plot:
            modules_dict[module].plot_data()
        return

    def plot_simulation(self):
        plt.figure('simulation')
        commands = modules_dict['command'].output_list_dict['command']
        states = modules_dict['first_order'].output_list_dict['FirstOrderInertialElement']
        plt.plot(np.array(commands)[:,0],np.array(commands)[:,1],label='command')
        plt.plot(np.array(states)[:,0],np.array(states)[:,1],label='state')
        plt.legend()
        return
    
    def test(self):
        self.simulate(600)
        # self.plot_modules()
        self.plot_simulation()
        return

def main():
    simu = Simulation()
    simu.test()
    plt.show()

if __name__ == '__main__':
    main()