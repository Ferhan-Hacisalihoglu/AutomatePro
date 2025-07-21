# AutomatePro: A Simple GUI Macro Recorder

AutomatePro is a user-friendly desktop application built with Python and PyQt6 that allows you to record and play back your mouse clicks and keyboard presses. It's a simple tool designed to automate repetitive tasks on your computer.

The application provides a clean and intuitive interface, with options for both dark and light modes to suit your preference.

-----

## Features

  * **Record & Playback**: Easily record a sequence of keyboard and mouse actions and play them back accurately.
  * **Repeat Actions**: Set the number of times you want the recorded macro to repeat.
  * **Save & Load**: Save your recorded macros to a `.json` file to use them later, or load previously saved macros.
  * **Real-time Action List**: See the actions you perform appear in a list in real-time as you record them.
  * **Dual Theme**: Switch between a modern dark mode and a clean light mode.
  * **Status Bar**: Get clear feedback on the application's current state (e.g., "Recording...", "Playback finished.", "Ready.").
  * **Safe Threading**: The playback process runs in a separate thread, so the application remains responsive and doesn't freeze. You can also stop the playback at any time.

-----

## How to Use

1.  **Prerequisites**: Make sure you have Python installed. Then, install the required libraries:

    ```bash
    pip install PyQt6 pynput
    ```

2.  **Run the Application**:

    ```bash
    python AutomatePro.py
    ```

3.  **Recording**:

      * Click the **"Start Recording"** button.
      * Perform any mouse clicks or key presses you want to automate. You will see them appear in the "Recorded Actions" list.
      * Click the **"Stop Recording"** button when you are finished.

4.  **Playback**:

      * After stopping the recording, the **"Play"** button will become active.
      * Use the **"Repeat Count"** spinbox to set how many times the macro should run.
      * Click **"Play"** to start the automation. The list will highlight each action as it is performed.
      * You can click **"Stop Playback"** at any time to interrupt the process.

5.  **Saving and Loading**:

      * Click **"Save"** to save your current list of actions to a file.
      * Click **"Load"** to open a previously saved macro file. The actions will appear in the list, ready for playback.

-----

## Technologies Used

  * **Python 3**
  * **PyQt6**: For the graphical user interface (GUI).
  * **Pynput**: For listening to and controlling mouse and keyboard input.
