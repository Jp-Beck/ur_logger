# ur_logger
Real-time GUI-based Custom Log Data Extractor for Universal Robots
# JP-Beck UR Logger

## Description
JP-Beck UR Logger is a graphical logging tool for Universal Robots. It provides an easy-to-use interface to log data and monitor the system state in real-time. The application is built using Python with the Tkinter library for the graphical interface, the xmlrpc library for communication, and the standard logging library for logging purposes.

## Features
1. **User-friendly interface**: The application has a simple and intuitive GUI with buttons for selecting the log folder, starting logging, and exiting the program. It also displays the IP address of the computer on the screen.
2. **Real-time log display**: The log messages are displayed in real-time in the output window of the application.
3. **Multithreading**: The application is designed to handle multiple threads for updating the GUI and running the main logic.
4. **XML-RPC server**: The application uses an XML-RPC server to receive data from the UR robot and log it in the specified log file.
5. **Cross-platform compatibility**: The application is compatible with Windows, macOS, and Linux operating systems.

## Usage
1. Run the `main.py` file to launch the JP-Beck UR Logger application.
2. Click on the "Select Folder" button to choose the folder where the log file will be saved.
3. Click on the "Start Logging" button to start logging the data received from the UR robot.
4. Monitor the log messages in real-time in the output window of the application.
5. Click on the "Exit Program" button to close the application.

**Note**: Make sure to have Python and the necessary libraries (Tkinter and xmlrpc) installed on your system before running the application.

Please refer to the README file for more information on installation and dependencies.
