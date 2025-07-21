import sys
import threading
import time
import json
import base64
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QListWidget, QLabel, QSpinBox, QHBoxLayout,
                             QFileDialog, QGridLayout, QStatusBar)
from PyQt6.QtCore import pyqtSignal, QObject

from pynput import mouse, keyboard

class WorkerSignals(QObject):
    action_added = pyqtSignal(str)
    playback_highlight = pyqtSignal(int)
    playback_finished = pyqtSignal()
    status_update = pyqtSignal(str)

class AutomatePro(QMainWindow):
    def __init__(self):
        super().__init__()

        self.recorded_actions = []
        self.is_recording = False
        self.stop_playback_flag = False
        self.keyboard_listener = None
        self.mouse_listener = None
        self.signals = WorkerSignals()
        self.is_dark_mode = True

        self.initUI()

    def initUI(self):
        self.setWindowTitle("AutomatePro")
        self.setGeometry(200, 200, 550, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)

        self.theme_button = QPushButton("Switch to Light Mode")
        theme_layout = QHBoxLayout()
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_button)
        self.grid_layout.addLayout(theme_layout, 0, 0, 1, 2)

        self.record_button = QPushButton("Start Recording")
        self.stop_button = QPushButton("Stop Recording")
        self.play_button = QPushButton("Play")
        self.stop_playback_button = QPushButton("Stop Playback")
        self.save_button = QPushButton("Save")
        self.load_button = QPushButton("Load")

        self.iter_label = QLabel("Repeat Count:")
        self.iter_spinbox = QSpinBox()
        self.iter_spinbox.setMinimum(1)
        self.iter_spinbox.setValue(1)

        self.action_list_widget = QListWidget()

        self.grid_layout.addWidget(self.record_button, 1, 0)
        self.grid_layout.addWidget(self.stop_button, 1, 1)
        self.grid_layout.addWidget(self.play_button, 2, 0)
        self.grid_layout.addWidget(self.stop_playback_button, 2, 1)
        self.grid_layout.addWidget(self.save_button, 3, 0)
        self.grid_layout.addWidget(self.load_button, 3, 1)
        
        iter_layout = QHBoxLayout()
        iter_layout.addWidget(self.iter_label)
        iter_layout.addWidget(self.iter_spinbox)
        self.grid_layout.addLayout(iter_layout, 4, 0, 1, 2)

        self.grid_layout.addWidget(QLabel("Recorded Actions:"), 5, 0, 1, 2)
        self.grid_layout.addWidget(self.action_list_widget, 6, 0, 1, 2)
        
        self.theme_button.clicked.connect(self.toggle_theme)
        self.record_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.play_button.clicked.connect(self.play_recording)
        self.stop_playback_button.clicked.connect(self.request_stop_playback)
        self.save_button.clicked.connect(self.save_recording)
        self.load_button.clicked.connect(self.load_recording)
        
        self.signals.action_added.connect(self.add_action_to_list)
        self.signals.playback_highlight.connect(self.highlight_action)
        self.signals.playback_finished.connect(self.on_playback_finished)
        self.signals.status_update.connect(self.update_status)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.update_status("Ready.")

        self.stop_button.setEnabled(False)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.stop_playback_button.setEnabled(False)
        
        self.apply_theme()

    def get_dark_theme_qss(self):
        up_arrow_white = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="5"><polygon points="5,0 10,5 0,5" fill="#ecf0f1"/></svg>').decode('utf-8')
        down_arrow_white = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="5"><polygon points="0,0 10,0 5,5" fill="#ecf0f1"/></svg>').decode('utf-8')
        
        return f"""
            QMainWindow, QWidget {{ background-color: #2c3e50; color: #ecf0f1; }}
            QPushButton {{ background-color: #34495e; border: 1px solid #2c3e50; padding: 8px; border-radius: 5px; text-align: center; }}
            QPushButton:hover {{ background-color: #4a6278; }}
            QPushButton:pressed {{ background-color: #2a3a4a; }}
            QPushButton:disabled {{ background-color: #525252; color: #999999; }}
            QListWidget {{ background-color: #34495e; border: 1px solid #2c3e50; border-radius: 5px; }}
            QListWidget::item:selected {{ background-color: #3498db; }}
            QLabel {{ color: #ecf0f1; }}
            QSpinBox {{ background-color: #34495e; border: 1px solid #2c3e50; border-radius: 5px; padding: 2px; color: #ecf0f1; }}
            QSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 16px; border-left: 1px solid #2c3e50; border-top-right-radius: 5px; }}
            QSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 16px; border-left: 1px solid #2c3e50; border-bottom-right-radius: 5px; }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background-color: #4a6278; }}
            QSpinBox::up-arrow {{ image: url(data:image/svg+xml;base64,{up_arrow_white}); width: 10px; height: 5px; }}
            QSpinBox::down-arrow {{ image: url(data:image/svg+xml;base64,{down_arrow_white}); width: 10px; height: 5px; }}
            QStatusBar {{ color: #ecf0f1; font-size: 9pt; }}
        """

    def get_light_theme_qss(self):
        up_arrow_black = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="5"><polygon points="5,0 10,5 0,5" fill="#000000"/></svg>').decode('utf-8')
        down_arrow_black = base64.b64encode(b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="5"><polygon points="0,0 10,0 5,5" fill="#000000"/></svg>').decode('utf-8')

        return f"""
            QMainWindow, QWidget {{ background-color: #f0f0f0; color: #000000; }}
            QPushButton {{ background-color: #e1e1e1; border: 1px solid #adadad; padding: 8px; border-radius: 5px; text-align: center; }}
            QPushButton:hover {{ background-color: #e5e5e5; border: 1px solid #0078d7;}}
            QPushButton:pressed {{ background-color: #c6c6c6; }}
            QPushButton:disabled {{ background-color: #d3d3d3; color: #a0a0a0; }}
            QListWidget {{ background-color: #ffffff; border: 1px solid #c2c2c2; border-radius: 5px; }}
            QListWidget::item:selected {{ background-color: #0078d7; color: #ffffff; }}
            QLabel {{ color: #000000; }}
            QSpinBox {{ background-color: #ffffff; border: 1px solid #c2c2c2; border-radius: 5px; padding: 2px; color: #000000; }}
            QSpinBox::up-button {{ subcontrol-origin: border; subcontrol-position: top right; width: 16px; border-left: 1px solid #c2c2c2; border-top-right-radius: 5px; }}
            QSpinBox::down-button {{ subcontrol-origin: border; subcontrol-position: bottom right; width: 16px; border-left: 1px solid #c2c2c2; border-bottom-right-radius: 5px; }}
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background-color: #e5e5e5; }}
            QSpinBox::up-arrow {{ image: url(data:image/svg+xml;base64,{up_arrow_black}); width: 10px; height: 5px; }}
            QSpinBox::down-arrow {{ image: url(data:image/svg+xml;base64,{down_arrow_black}); width: 10px; height: 5px; }}
            QStatusBar {{ color: #000000; font-size: 9pt; }}
        """
    
    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(self.get_dark_theme_qss())
            self.theme_button.setText("Switch to Light Mode")
        else:
            self.setStyleSheet(self.get_light_theme_qss())
            self.theme_button.setText("Switch to Dark Mode")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_theme()

    def update_status(self, message):
        self.statusBar.showMessage(message)

    def add_action_to_list(self, action_text):
        self.action_list_widget.addItem(action_text)
        self.action_list_widget.scrollToBottom()

    def highlight_action(self, index):
        self.action_list_widget.setCurrentRow(index)

    def start_recording(self):
        self.is_recording = True
        self.recorded_actions = []
        self.action_list_widget.clear()
        
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.stop_playback_button.setEnabled(False)
        self.theme_button.setEnabled(False)
        
        self.signals.status_update.emit("Recording...")
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    def stop_recording(self):
        if not self.is_recording:
            return
            
        self.is_recording = False
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.load_button.setEnabled(True)
        self.theme_button.setEnabled(True)
        if self.recorded_actions:
            self.play_button.setEnabled(True)
            self.save_button.setEnabled(True)
        
        self.signals.status_update.emit("Recording stopped. Ready.")

    def play_recording(self):
        if not self.recorded_actions:
            return

        self.stop_playback_flag = False
        self.record_button.setEnabled(False)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.stop_playback_button.setEnabled(True)
        self.theme_button.setEnabled(False)
        
        iterations = self.iter_spinbox.value()
        self.signals.status_update.emit(f"Playing back recording {iterations} time(s)...")

        playback_thread = threading.Thread(target=self.run_playback, args=(iterations,))
        playback_thread.start()

    def request_stop_playback(self):
        self.signals.status_update.emit("Stopping playback...")
        self.stop_playback_flag = True

    def on_playback_finished(self):
        self.signals.status_update.emit("Playback finished.")
        self.record_button.setEnabled(True)
        self.load_button.setEnabled(True)
        self.stop_playback_button.setEnabled(False)
        self.theme_button.setEnabled(True)
        if self.recorded_actions:
            self.play_button.setEnabled(True)
            self.save_button.setEnabled(True)

    def save_recording(self):
        if not self.recorded_actions:
            return
        
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Recording", "", "JSON Files (*.json)")
        if filePath:
            with open(filePath, 'w') as f:
                json.dump(self.recorded_actions, f, indent=4)
            self.signals.status_update.emit(f"Recording saved to: {filePath}")

    def load_recording(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Load Recording", "", "JSON Files (*.json)")
        if filePath:
            try:
                with open(filePath, 'r') as f:
                    self.recorded_actions = json.load(f)
                self.populate_list_from_actions()
                if self.recorded_actions:
                    self.play_button.setEnabled(True)
                    self.save_button.setEnabled(True)
                self.signals.status_update.emit(f"Recording loaded from: {filePath}")
            except (json.JSONDecodeError, IOError) as e:
                self.signals.status_update.emit(f"Error: Could not load file - {e}")
                self.recorded_actions = []
                self.action_list_widget.clear()

    def format_action_to_string(self, action):
        if action['type'] == 'key_press':
            return f"Key Press: {action['key']}"
        elif action['type'] == 'mouse_click':
            btn_name = action['button'].replace('Button.', '').capitalize()
            return f"Mouse Click: ({action['x']}, {action['y']}) - {btn_name}"
        return "Unknown Action"

    def populate_list_from_actions(self):
        self.action_list_widget.clear()
        for action in self.recorded_actions:
            action_text = self.format_action_to_string(action)
            self.action_list_widget.addItem(action_text)

    def on_press(self, key):
        if self.is_recording:
            action_time = time.time()
            try:
                action = {'type': 'key_press', 'key': key.char, 'time': action_time}
            except AttributeError:
                action = {'type': 'key_press', 'key': str(key), 'time': action_time}
            
            self.recorded_actions.append(action)
            self.signals.action_added.emit(self.format_action_to_string(action))

    def on_click(self, x, y, button, pressed):
        if self.is_recording and pressed:
            action_time = time.time()
            action = {'type': 'mouse_click', 'x': x, 'y': y, 'button': str(button), 'time': action_time}
            self.recorded_actions.append(action)
            self.signals.action_added.emit(self.format_action_to_string(action))

    def run_playback(self, iterations):
        try:
            mouse_ctrl = mouse.Controller()
            keyboard_ctrl = keyboard.Controller()

            for i in range(iterations):
                if self.stop_playback_flag:
                    break
                
                self.signals.status_update.emit(f"Executing iteration {i + 1}/{iterations}...")
                
                if not self.recorded_actions:
                    break
                
                if self.recorded_actions:
                    last_action_time = self.recorded_actions[0]['time']
                else:
                    last_action_time = time.time()

                for index, action in enumerate(self.recorded_actions):
                    if self.stop_playback_flag:
                        break

                    delay = action['time'] - last_action_time
                    if delay > 0:
                        time.sleep(delay)
                    last_action_time = action['time']

                    self.signals.playback_highlight.emit(index)
                    
                    if self.stop_playback_flag:
                        break

                    if action['type'] == 'mouse_click':
                        mouse_ctrl.position = (action['x'], action['y'])
                        btn = mouse.Button.left if 'left' in action['button'] else mouse.Button.right if 'right' in action['button'] else mouse.Button.middle
                        mouse_ctrl.click(btn, 1)
                    
                    elif action['type'] == 'key_press':
                        key_to_press = action['key']
                        if key_to_press.startswith('Key.'):
                            key_name = key_to_press.split('.')[-1]
                            key_to_press = getattr(keyboard.Key, key_name, key_name)
                        
                        if key_to_press:
                            keyboard_ctrl.press(key_to_press)
                            keyboard_ctrl.release(key_to_press)
                
                if i < iterations - 1 and not self.stop_playback_flag:
                    time.sleep(1) 

        finally:
            self.signals.playback_finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomatePro()
    window.show()
    sys.exit(app.exec())