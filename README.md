# 🎛️ AutomatePro: A Simple and Powerful GUI-Based Macro Recorder

AutomatePro is a lightweight and intuitive desktop application built with Python and PyQt6 that lets you easily record and replay your mouse clicks and keyboard actions. Whether you're automating repetitive tasks or creating complex workflows, AutomatePro is your go-to tool for desktop automation.

With a focus on both power and ease-of-use, AutomatePro supports action editing, smart delay capture, and a modern interface, making it the perfect tool for your automation needs.

## 🚀 Features

  * **🎥 Record & Playback**: Precisely record your keyboard and mouse actions and replay them with accurate timing.
  * **✏️ Edit & Delete Actions**: Fine-tune your macros after recording. Right-click any action to open the edit dialog and modify its **delay, key, or mouse coordinates**, or simply delete it.
  * **⏱️ Smart Delay Recording**: Automatically captures the time delays between your actions, resulting in more natural and reliable playback.
  * **🔦 Live Playback Highlighting**: Visually track your macro's execution. The currently running action is **highlighted in the list**, so you always know what's happening.
  * **🔁 Loop Automation**: Easily set how many times you want your macro to repeat using the modern stepper controls.
  * **💾 Save & Load Macros**: Export your recorded workflows to `.json` files and load them back anytime.
  * **🧾 Enhanced Action List**: Watch your actions, including their specific delays, appear in the list instantly as you record.
  * **🎨 Modern Theming**: Switch between a sleek dark mode and a clean light mode with a single click to match your preference.
  * **📣 Status Bar Notifications**: Stay informed with clear status messages like “Recording...”, “Playing...”, or “Ready.”
  * **🧵 Safe Multithreaded Playback**: Playback runs on a separate thread to keep the UI responsive. You can safely interrupt the process at any time without freezing the app.

-----

## 📚 How to Use

**1. Install Dependencies**

Make sure Python 3 is installed. Then, install the required packages:

```bash
pip install PyQt6 pynput
```

**2. Record Your Macro**

  * Click **"Record"** to start.
  * Perform your mouse clicks and key presses.
  * Click **"Stop"** when you are finished.
    Your actions will appear in the "Recorded Actions" list.

**3. Edit Your Macro (Optional)**

  * **Right-click** on an action in the list to open the context menu.
  * Select **"Edit"** to modify its properties (like delay or coordinates) or **"Delete"** to remove it.

**4. Play the Macro**

  * Set the number of loops using the **"Repeats"** control.
  * Click **"Play"** to start the playback.
  * Use **"Stop Playback"** to cancel the process at any time.

**5. Save or Load Macros**

  * Click **"Save"** to export your actions to a `.json` file.
  * Click **"Load"** to open a previously saved macro.

-----

## 🛠 Technologies Used

  * **Python 3**
  * **PyQt6** – For building the user interface.
  * **Pynput** – For capturing and simulating keyboard/mouse input.

-----

## 💡 Ideal Use Cases

  * Automating repetitive data entry.
  * Running multi-step workflows.
  * Refining and perfecting recorded automation scripts.
  * Creating quick UI demos or tests.
  * Saving time on routine desktop tasks.
