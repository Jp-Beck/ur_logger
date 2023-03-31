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

