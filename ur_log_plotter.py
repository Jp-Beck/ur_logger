import matplotlib.pyplot as plt
import math
import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

module_path = os.path.abspath(__file__)
folder_path = os.path.dirname(module_path)

class Plot:
    def __init__(self, set_point, axis, log_file, y_label, title, axis_index, angle = False):
        self.set_point = set_point
        self.axis = axis
        self.log_file = log_file
        self.y_label = y_label
        self.title = title
        self.angle = angle
        self.axis_index = axis_index
    
    def switch_example(self):
        switcher = {
            0: "X",
            1: "Y",
            2: "Z",
            3: "Rx",
            4: "Ry",
            5: "Rz",
        }
        return switcher.get(self.axis, "nothing")

    def read_log_file(self):
        with open(self.log_file, 'r') as f:
            lines = f.readlines()
            if self.angle:
                self.distances = [(abs(self.set_point) - abs(float(line.split()[self.axis].rstrip(','))))*180/math.pi for line in lines]
            else:
                self.distances = [(abs(self.set_point) - abs(float(line.split()[self.axis].rstrip(','))))*1000 for line in lines]

    def plot(self):
        fig, ax = plt.subplots()
        ax.bar(range(len(self.distances)), self.distances)
        #for i, v in enumerate(self.distances):
            #ax.annotate(str(v), xy=(i, v), ha='center', va='bottom')
        ax.set_xlabel('Attempts')
        ax.set_ylabel(self.y_label)
        ax.set_xticks(range(len(self.distances)))
        ax.set_xticklabels(range(1, len(self.distances) + 1))
        ax.set_title(self.title)
        ax.axhline(y=0, color='red', linestyle='--', label=f'Set point({self.switch_example()} Axis):{self.set_point}')
        ax.axhline(y=0.95 if self.axis <= 2 else 0.3, color='green', linestyle='-', label='Upper range limit (0.95 mm)' if self.axis <= 2 else 'Upper range limit (0.3 degrees)') 
        ax.axhline(y=-0.2635 if self.axis <= 2 else -0.3, color='green', linestyle='-', label='Lower range limit (-0.2635 mm)' if self.axis <= 2 else 'Lower range limit (-0.3 degrees)')
        ax.set_ylim(-1, 1)  # Set the y-axis range to always be between -1 and 1
        ax.grid(True, linestyle='--', alpha=0.5)


        plt.legend()
        # plt.show() #uncomment if you want to show the plot on the screen
        global saved_name
        # Save the plot as a file in the current dirrectory
        plt.savefig(f"{self.title}.png", dpi= 600)

        # Close the plot to free up memory
        plt.close(fig)

class PlotProcessor:
    def __init__(self, folder_path):
        self.folder_path = folder_path

    def switch_example(self, axis_index):
        switcher = {
            0: "X",
            1: "Y",
            2: "Z",
            3: "Rx",
            4: "Ry",
            5: "Rz",
        }
        return switcher.get(axis_index, "nothing")

    def get_plot_info(self, axis_index, filename):
        unit = '(degree)' if axis_index > 2 else '(mm)'
        title = f'Difference between set point vs. Test for {self.switch_example(axis_index)} in {filename}'
        global saved_name
        saved_name = f"{self.switch_example(axis_index)}_in_{filename}_{axis_index}"
        angle = axis_index > 2
        return unit, title, angle

    def process_plot(self, plot):
        plot.read_log_file()
        plot.plot()
        print(f"Saved plot as {saved_name}.png")

    def run(self):
        max_workers = os.cpu_count()
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.log'):
                print(f"Processing log file: {filename}")
                filepath = str(os.path.join(self.folder_path, filename))
                with open(filepath, 'r') as f:
                    subprocess.run(['sed', '-i', 's/^2023.*: //', filepath])
                    subprocess.run(['sed', '-i', 's/^2023.*> //', filepath])
                    data = f.read()
                    values = data.split()[0:6]
                    set_point = [float(value.rstrip(',')) for value in values]
                log_file = filepath

                plots = [
                    Plot(set_point[0], 0, log_file, *self.get_plot_info(0, filename)),
                    Plot(set_point[1], 1, log_file, *self.get_plot_info(1, filename)),
                    Plot(set_point[2], 2, log_file, *self.get_plot_info(2, filename)),
                    Plot(set_point[3], 3, log_file, *self.get_plot_info(3, filename)),
                    Plot(set_point[4], 4, log_file, *self.get_plot_info(4, filename)),
                    Plot(set_point[5], 5, log_file, *self.get_plot_info(5, filename)),
                ]

                print(f"Created {len(plots)} plots for {filename}")

                with ProcessPoolExecutor(max_workers=max_workers) as executor:
                    executor.map(self.process_plot, plots)


if __name__ == "__main__":
    plot_processor = PlotProcessor(folder_path)
    plot_processor.run()
