## Summary

This code is a Python-based macro automation tool that allows users to execute a series of keyboard commands with specified multipliers, intervals, and optional specific sleep times between commands. Users can enter a sequence of commands, set the number of times the entire sequence will be executed, and the default sleep time between commands. The program utilizes the tkinter library to create a graphical user interface (GUI) for easy input and PyAutoGUI for typing out the command.

## Skills used

- **Threading**: The code uses Python's `threading` module to run the macro program in a separate thread, enabling the user to stop the execution of the macro at any time.
- **Tkinter**: The code uses the `tkinter` library to create a graphical user interface (GUI) for the user to interact with the program.
- **Custom Styling**: The tkinter GUI components are extensively customized using dictionaries containing style properties such as colors, fonts, and borders, giving the application a unique and polished appearance(dark mode).
- **PyAutoGUI**: The code makes extensive use of the `pyautogui` library to simulate keyboard inputs and manage command execution, allowing for seamless interaction with other applications and automating tasks.
- **Grid System**: The code organizes the GUI components using the tkinter grid system, providing a clean and orderly layout for the user interface. This also makes it easier to add or modify components and maintain a consistent appearance.


## Features

- **Customizable Command Sequence**: Users can input a sequence of commands and set multipliers for each command to be executed consecutively in the specified order.
- **Individual Sleep Time**: Users can set a specific sleep time for each command, allowing for greater control over the delay between commands.
- **Global Sleep Time**: Users can set a global sleep time that will be applied between commands where no specific sleep time is set.
- **Iterations**: Users can specify the number of times the entire command sequence will be executed.
- **Start/Stop Functionality**: The program can be started and stopped at any time using the "Run" and "Stop" buttons in the GUI.
- **Reset**: Users can reset all input fields to their default state using the "Reset" button in the GUI.
- **Output Log**: The program displays an output log within the GUI, showing the progress of the macro execution and any relevant messages.
- **Custom Checkboxes**: The code includes a custom Checkbox class for creating custom-styled checkboxes within the tkinter GUI.
- **Scalable GUI**: The GUI is designed to scale appropriately on high-DPI displays.
