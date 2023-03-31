#!/usr/bin/env python
# main.py

"""
# Author: "Beck Isakov"
# Contact: "jp-beck@outlook.com"
"""

import os
import sys
import time
import datetime
import platform
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
import queue
import logging
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client as xmlrpclib

class MyLoggerGUI:
    def __init__(self, master):
        self.master = master
        master.title("JP-Beck UR Logger")
        

        self.select_folder_btn = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.select_folder_btn.pack(pady=10)

        self.start_logging_btn = tk.Button(master, text="Start Logging", command=self.start_logging, state="disabled")
        self.start_logging_btn.pack(pady=10)

        self.exit_btn = tk.Button(master, text="Exit Program", command=root.quit)
        self.exit_btn.pack(pady=10, padx=30)

        self.output_text = tk.Text(master, height=10, width=60)
        self.output_text.pack(pady=10)

        self.logger = None
        self.server = None
        self.log_filename = ""
        

        self.output_queue = queue.Queue()
        self.gui_update_interval = 100  # milliseconds
        self.update_gui_event = threading.Event()

        # Create a thread that periodically updates the GUI with new log messages
        self.gui_update_thread = threading.Thread(target=self.update_gui_thread_func, daemon=True)
        self.gui_update_thread.start()

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.log_filename = os.path.join(folder_selected, _create_log_file())
            self.start_logging_btn.configure(state="normal")

    def start_logging(self):
        if self.log_filename:
            self.create_logger_and_server()
            # Start the main logic in a separate process
            def run_server():
                sys.stdout.write("\n --Main Program Running-- \n")
                self.output_text.insert(tk.END, "--Main Program Running--\n")
                self.output_text.insert(tk.END, f"Listening on port 33000...\n")
                self.output_text.see(tk.END)

                self.server.start()

            # Start the main logic process
            process = threading.Thread(target=run_server, daemon=True)
            process.start()

            self.start_logging_btn.configure(state="disabled")
        else:
            messagebox.showwarning("Folder not selected", "Please select a folder first.")

    def exit_program(self):
        if self.server:
            self.server.stop()
        if hasattr(self, "process") and self.process.is_alive():
            self.process.join()
        self.master.destroy()
        sys.exit()


    def update_gui_thread_func(self):
        while True:
            self.update_gui_event.wait()
            while not self.output_queue.empty():
                log_message = self.output_queue.get()
                self.output_text.insert(tk.END, log_message + '\n')
                self.output_text.see(tk.END)
            self.update_gui_event.clear()
            time.sleep(self.gui_update_interval / 1000)

    def create_logger_and_server(self):
        self.logger = Logger(self.log_filename)

        self.server = RPCServer("", 33000)

        # RPC functions:
        @self.server.register_function
        def negBool(boo):
            self.logger.log(f"Received the boolean: {boo}")
            return not boo

        @self.server.register_function
        def yuki_log(value, info="INFO"):
            try:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                if isinstance(value, dict) and all(key in value for key in ("rx", "ry", "rz", "x", "y", "z")):
                    formatted_value = ", ".join(str(value[key]) for key in ("x", "y", "z", "rx", "ry", "rz"))
                elif isinstance(value, str):
                    formatted_value = value
                else:
                    formatted_value = str(value)
                log_message = f"{info}|> {formatted_value}"
                self.logger.log(log_message)
                self.output_queue.put(log_message)
                self.update_gui_event.set()
            except IOError as e:
                print(f"Could not write the file: {e}")
class Logger:
    def __init__(self, log_filename):
        self.log_filename = log_filename
        self.logger = logging.getLogger('myLogger')
        self.logger.setLevel(logging.INFO)
        self._create_file_handler()

    def _create_file_handler(self):
        fh = logging.FileHandler(self.log_filename)
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def log(self, message):
        self.logger.info(message)


class RPCServer:
    def __init__(self, host, port):
        self.server = SimpleXMLRPCServer((host, port), allow_none=True)
        self.server.RequestHandlerClass.protocol_version = "HTTP/1.1"
        self.functions = {}

    def register_function(self, func):
        self.functions[func.__name__] = func
        self.server.register_function(func, func.__name__)

    def start(self):
        sys.stdout.write(f"Listening on port {self.server.server_address[1]}...\n")
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

    def stop(self):
        self.server.shutdown()

    def call(self, func_name, *args):
        if func_name in self.functions:
            return self.functions[func_name](*args)
        else:
            raise ValueError(f"{func_name} not found in registered functions.")


class StdoutRedirector:
    def __init__(self, widget, buffer_time=200):
        self.widget = widget
        self.buffer_time = buffer_time
        self.buffer = ""

    def write(self, text):
        self.buffer += text

    def flush(self):
        if self.buffer:
            self.widget.insert(tk.END, self.buffer)
            self.widget.see(tk.END)
            self.buffer = ""

    def start_flush_timer(self):
        self.flush_timer = threading.Timer(self.buffer_time / 1000, self.flush)
        self.flush_timer.start()

    def reset_flush_timer(self):
        self.flush_timer.cancel()
        self.start_flush_timer()


def _create_log_file():
    current_time = time.strftime("%Y-%m-%d")
    filename = f"log_{current_time}.log"
    two_days_ago = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    two_days_ago_file = f"log_{two_days_ago}.log"
    return filename


def get_ip_addresses():
    ip_addresses = []
    if platform.system() == "Windows":
        # Windows command
        output = subprocess.check_output(["ipconfig"]).decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "IPv4" in line:
                ip_address = line.split(":")[-1].strip()
                ip_addresses.append(ip_address)
    else:
        # Linux/Mac command
        output = subprocess.check_output(["ifconfig"]).decode("utf-8")
        lines = output.split("\n")
        for line in lines:
            if "inet " in line:
                ip_address = line.split()[1]
                if ip_address != "127.0.0.1":
                    ip_addresses.append(ip_address)
    return ip_addresses

if __name__ == '__main__':
    root = tk.Tk()
    # Set the icon bitmap
    try:
        if "posix" == os.name:
            root.wm_iconbitmap(bitmap="@jp-beck.xbm")
        else:
            root.wm_iconbitmap(bitmap="jp-beck.ico")
    except tk.TclError:
        # If the icon file cannot be loaded or found, log an error message and continue running
        logging.error("Failed to load icon file")

    my_logger_gui = MyLoggerGUI(root)
    # Get the IP address of the computer
    ip_address = get_ip_addresses()

    # Create a label to display the IP address
    ip_label = tk.Label(text=f"IP Address: {ip_address}")
    ip_label.pack()
    root.mainloop()
