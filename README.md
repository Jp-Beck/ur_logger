# JP-Beck UR Logger
Real-time GUI-based Custom Log Data Extractor for Universal Robots
## Description
JP-Beck UR Logger is a graphical logging tool for Universal Robots. It provides an easy-to-use interface to log data and monitor the system state in real-time. The application is built using Python with the Tkinter library for the graphical interface, the xmlrpc library for communication, and the standard logging library for logging purposes.

## Features
1. **User-friendly interface**: The application has a simple and intuitive GUI with buttons for selecting the log folder, starting logging, and exiting the program. It also displays the IP address of the computer on the screen.
2. **Real-time log display**: The log messages are displayed in real-time in the output window of the application.
3. **Multithreading**: The application is designed to handle multiple threads for updating the GUI and running the main logic.
4. **XML-RPC server**: The application uses an XML-RPC server to receive data from the UR robot and log it in the specified log file.
5. **Cross-platform compatibility**: The application is compatible with Windows, macOS, and Linux operating systems.

## Usage
0. Instantiate the XML-RPC connection to your machine. 
Make sure you are on the same network with the robot.
The second IP address is the connectable address.
![screenshot_0025](https://user-images.githubusercontent.com/71532612/229045780-4a7a34eb-e737-4680-b1aa-38a5b0e8c540.png)

1. Run the `gui_logger.py` file to launch the JP-Beck UR Logger application.
2. Click on the "Select Folder" button to choose the folder where the log file will be saved.
3. Click on the "Start Logging" button to start logging the data received from the UR robot.
4. Monitor the log messages in real-time in the output window of the application.
5. Click on the "Exit Program" button to close the application.

![Screenshot from 2023-03-31 15-07-44](https://user-images.githubusercontent.com/71532612/229043782-5f3b9f3f-6b06-41a9-bbf2-24a6ffc5e34e.png)
![Screenshot from 2023-03-31 15-08-07](https://user-images.githubusercontent.com/71532612/229043805-351e0463-a996-4037-8741-24f67b54c9f6.png)
![Screenshot from 2023-03-31 15-08-25](https://user-images.githubusercontent.com/71532612/229043835-abd52047-2100-486c-86fc-a10148c3e76e.png)
![Screenshot from 2023-03-31 15-26-28](https://user-images.githubusercontent.com/71532612/229043854-de31e043-3fe3-4652-a711-d2c3459ce99f.png)

## Result
The log file is in the folder specified.

*2023-03-31 15:26:19,645 - TCP|> 0.17310623926225058, -0.4740799469716069, 0.07655795341205152, -2.427682771314296, 1.90687468989263, 0.035768804871035016
2023-03-31 15:26:20,880 - TCP|> 0.173136771685861, -0.4741064398166569, 0.07658990487910476, -2.42773733760848, 1.906828902335053, 0.03565147842553099*

[log_2023-03-31.log](https://github.com/Jp-Beck/ur_logger/files/11118950/log_2023-03-31.log)


**Note**: Make sure to have Python and the necessary libraries (Tkinter and xmlrpc) installed on your system before running the application.
**Note**: When you exit out of the logger program, the universal robot stops due to loss of connection
![screenshot_0026](https://user-images.githubusercontent.com/71532612/229045819-3021d6b7-92b4-4e67-b191-21dc40dbd281.png)

Please refer to the README file for more information on installation and dependencies.
Although there is a URScript, which allows you to add log message to the robot's support file, you need to 
save the support.zip file to a usb or ssh copy which is clumsy. 
> textmsg("Hello")
![screenshot_0028](https://user-images.githubusercontent.com/71532612/229051838-951eec6c-99ed-4fc4-8f26-b098bffd91fe.png)

# # Plot the logs - Bar Graph Plotter

If you would like to visualize the log data, referer to 'ur_plotter.py'

This Python script reads log files from a specified folder, processes them, and generates bar graphs to visualize the data. The generated plots are saved as PNG images in the same folder as the Python module.

## Usage
**__This program can be used to analyze the consistency of a vision system or judge the accuracy of a robot's joint movements.__**
1. Ensure that your log files are placed in the same folder as the Python module.
2. Run the script using your Python interpreter: `python ur_plotter.py`
3. The script will process each log file, create bar graphs for each data set, and save them as PNG images in the same folder.

## Features

- The script processes log files and creates plots for different axes (X, Y, Z, Rx, Ry, and Rz).
- It generates bar graphs with appropriate labels, titles, and legends.
- The bar graphs include a red dashed line representing the set point and green lines representing the upper and lower range limits.
- The plots are saved as high-resolution (600 dpi) PNG images.
- The script uses concurrent processing with the `ProcessPoolExecutor` to speed up the plotting process.

## Dependencies

- matplotlib: Used for generating the bar graphs.
- math: Used for mathematical operations.
- os: Used for file and folder operations.
- subprocess: Used for running shell commands.
- concurrent.futures: Used for concurrent processing.

## Classes

- `Plot`: Represents a single plot with methods for reading log files and generating the bar graph.
- `PlotProcessor`: Processes the log files and generates the plots using multiple threads.

## Note

- Make sure that the log files have the correct format for the script to work properly.
> subprocess.run(['sed', '-i', 's/^2023.*: //', filepath])

'sed' linux command has been used to clean up the datetime() from each line. However, it will not erase other data
- The script has been tested with Python 3.8 and above.

## Results
![Difference between set point vs  Test for X in 1p_x_y_30 log](https://user-images.githubusercontent.com/71532612/229064356-857bbf51-0051-4b2c-b10e-ede34184ac8d.png)
![Difference between set point vs  Test for Y in 1p_x_y_30 log](https://user-images.githubusercontent.com/71532612/229064363-b6ec57ef-491b-425b-8f59-9f6bc6a65afd.png)
![Difference between set point vs  Test for Z in 1p_x_y_30 log](https://user-images.githubusercontent.com/71532612/229064377-9cf41a65-61d0-462b-b7c2-9fe97b33744a.png)
![Difference between set point vs  Test for Rx in 1P_x_30 log](https://user-images.githubusercontent.com/71532612/229064344-43ac7311-33fe-4c2e-b088-65b7323a5597.png)
![Difference between set point vs  Test for Ry in 1P_y_30 log](https://user-images.githubusercontent.com/71532612/229064315-01f0c287-6a77-4366-b5df-ef62e767a1f4.png)
![Difference between set point vs  Test for Rz in 1p_x_y_30 log](https://user-images.githubusercontent.com/71532612/229064352-5390c26e-5d86-4e9f-9b4d-49b51bac21bb.png)

**Note**
'set_point' is the waypoint the Universal Robot's TCP is expected to be.
'Range limits' are the allowed error interval.

![Screenshot from 2023-03-31 18-06-18](https://user-images.githubusercontent.com/71532612/229078079-93c32148-2825-4e90-9ba1-b38a8d13f741.png)
