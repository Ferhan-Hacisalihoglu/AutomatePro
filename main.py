import sys
import threading
import time
import json
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QWidget, QListWidget, QLabel, QSpinBox, QHBoxLayout,
                             QFileDialog, QGridLayout, QStatusBar, QDialog,
                             QFormLayout, QLineEdit, QDialogButtonBox, QDoubleSpinBox,
                             QMenu)
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QPoint
from PyQt6.QtGui import QAction, QIcon, QFont

from pynput import mouse, keyboard

class EditActionDialog(QDialog):
    def __init__(self, action, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Action")
        self.action = action
        
        form_layout = QFormLayout(self)
        form_layout.setSpacing(10)
        form_layout.setContentsMargins(15, 15, 15, 15)
        
        # Delay input with custom buttons
        self.delay_spinbox = QDoubleSpinBox()
        self.delay_spinbox.setMinimum(0.05)
        self.delay_spinbox.setMaximum(60.0)
        self.delay_spinbox.setSingleStep(0.05)
        self.delay_spinbox.setValue(action.get('delay', 1.0))
        self.delay_spinbox.setPrefix("Delay: ")
        self.delay_spinbox.setSuffix(" s")
        self.delay_spinbox.setButtonSymbols(QDoubleSpinBox.ButtonSymbols.NoButtons)
        delay_layout = QHBoxLayout()
        delay_inc_button = QPushButton()
        delay_inc_button.setIcon(QIcon.fromTheme("go-up"))
        delay_inc_button.setFixedSize(24, 24)
        delay_inc_button.clicked.connect(lambda: self.delay_spinbox.stepBy(1))
        delay_dec_button = QPushButton()
        delay_dec_button.setIcon(QIcon.fromTheme("go-down"))
        delay_dec_button.setFixedSize(24, 24)
        delay_dec_button.clicked.connect(lambda: self.delay_spinbox.stepBy(-1))
        delay_layout.addWidget(self.delay_spinbox)
        delay_layout.addWidget(delay_dec_button)
        delay_layout.addWidget(delay_inc_button)
        form_layout.addRow("Delay:", delay_layout)
        
        self.type_label = QLabel(f"Type: {action['type'].replace('_', ' ').title()}")
        self.type_label.setFont(QFont("Arial", 10))
        form_layout.addRow(self.type_label)
        
        if action['type'] == 'key_press':
            self.key_input = QLineEdit(str(action['key']))
            self.key_input.setPlaceholderText("Enter key")
            form_layout.addRow("Key:", self.key_input)
        elif action['type'] == 'mouse_click':
            # X coordinate input with custom buttons
            self.x_spinbox = QSpinBox()
            self.x_spinbox.setMaximum(9999)
            self.x_spinbox.setValue(action['x'])
            self.x_spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
            x_layout = QHBoxLayout()
            x_inc_button = QPushButton()
            x_inc_button.setIcon(QIcon.fromTheme("go-next"))
            x_inc_button.setFixedSize(24, 24)
            x_inc_button.clicked.connect(lambda: self.x_spinbox.stepBy(1))
            x_dec_button = QPushButton()
            x_dec_button.setIcon(QIcon.fromTheme("go-previous"))
            x_dec_button.setFixedSize(24, 24)
            x_dec_button.clicked.connect(lambda: self.x_spinbox.stepBy(-1))
            x_layout.addWidget(QLabel("X:"))
            x_layout.addWidget(self.x_spinbox)
            x_layout.addWidget(x_dec_button)
            x_layout.addWidget(x_inc_button)
            
            # Y coordinate input with custom buttons
            self.y_spinbox = QSpinBox()
            self.y_spinbox.setMaximum(9999)
            self.y_spinbox.setValue(action['y'])
            self.y_spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
            y_layout = QHBoxLayout()
            y_inc_button = QPushButton()
            y_inc_button.setIcon(QIcon.fromTheme("go-up"))
            y_inc_button.setFixedSize(24, 24)
            y_inc_button.clicked.connect(lambda: self.y_spinbox.stepBy(1))
            y_dec_button = QPushButton()
            y_dec_button.setIcon(QIcon.fromTheme("go-down"))
            y_dec_button.setFixedSize(24, 24)
            y_dec_button.clicked.connect(lambda: self.y_spinbox.stepBy(-1))
            y_layout.addWidget(QLabel("Y:"))
            y_layout.addWidget(self.y_spinbox)
            y_layout.addWidget(y_dec_button)
            y_layout.addWidget(y_inc_button)
            
            form_layout.addRow("X Position:", x_layout)
            form_layout.addRow("Y Position:", y_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        form_layout.addRow(button_box)

    def get_data(self):
        updated_action = self.action.copy()
        updated_action['delay'] = self.delay_spinbox.value()
        
        if self.action['type'] == 'key_press':
            updated_action['key'] = self.key_input.text()
        elif self.action['type'] == 'mouse_click':
            updated_action['x'] = self.x_spinbox.value()
            updated_action['y'] = self.y_spinbox.value()
            
        return updated_action

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
        self.last_action_time = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AutomatePro")
        self.setGeometry(200, 200, 600, 750)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Header with theme toggle
        header_layout = QHBoxLayout()
        title_label = QLabel("AutomatePro")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        self.theme_button = QPushButton("Light Mode")
        self.theme_button.setIcon(QIcon.fromTheme("weather-clear"))
        header_layout.addWidget(self.theme_button)
        main_layout.addLayout(header_layout)

        # Control buttons
        control_layout = QGridLayout()
        control_layout.setSpacing(10)
        
        self.record_button = QPushButton("Record")
        self.record_button.setIcon(QIcon.fromTheme("media-record"))
        self.stop_button = QPushButton("Stop")
        self.stop_button.setIcon(QIcon.fromTheme("media-playback-stop"))
        self.play_button = QPushButton("Play")
        self.play_button.setIcon(QIcon.fromTheme("media-playback-start"))
        self.stop_playback_button = QPushButton("Stop Playback")
        self.stop_playback_button.setIcon(QIcon.fromTheme("media-playback-pause"))
        self.save_button = QPushButton("Save")
        self.save_button.setIcon(QIcon.fromTheme("document-save"))
        self.load_button = QPushButton("Load")
        self.load_button.setIcon(QIcon.fromTheme("document-open"))

        # Repeat count section
        iter_layout = QHBoxLayout()
        self.iter_label = QLabel("Repeats:")
        self.iter_spinbox = QSpinBox()
        self.iter_spinbox.setMinimum(1)
        self.iter_spinbox.setValue(1)
        self.iter_spinbox.setFixedWidth(80)
        self.iter_spinbox.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self.inc_button = QPushButton()
        self.inc_button.setIcon(QIcon.fromTheme("go-up"))
        self.inc_button.setFixedSize(32, 32)
        self.inc_button.clicked.connect(lambda: self.iter_spinbox.stepBy(1))
        self.dec_button = QPushButton()
        self.dec_button.setIcon(QIcon.fromTheme("go-down"))
        self.dec_button.setFixedSize(32, 32)
        self.dec_button.clicked.connect(lambda: self.iter_spinbox.stepBy(-1))
        iter_layout.addWidget(self.iter_label)
        iter_layout.addWidget(self.dec_button)
        iter_layout.addWidget(self.iter_spinbox)
        iter_layout.addWidget(self.inc_button)
        iter_layout.addStretch()

        control_layout.addWidget(self.record_button, 0, 0)
        control_layout.addWidget(self.stop_button, 0, 1)
        control_layout.addWidget(self.play_button, 1, 0)
        control_layout.addWidget(self.stop_playback_button, 1, 1)
        control_layout.addWidget(self.save_button, 2, 0)
        control_layout.addWidget(self.load_button, 2, 1)
        main_layout.addLayout(control_layout)
        main_layout.addLayout(iter_layout)

        # Action list
        actions_label = QLabel("Recorded Actions (Right-click to edit/delete):")
        actions_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        main_layout.addWidget(actions_label)
        
        self.action_list_widget = QListWidget()
        self.action_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.action_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        self.action_list_widget.setAlternatingRowColors(True)
        self.action_list_widget.setMinimumHeight(400)
        main_layout.addWidget(self.action_list_widget)

        # Status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.update_status("Ready")

        # Connect signals
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

        # Initial button states
        self.stop_button.setEnabled(False)
        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.stop_playback_button.setEnabled(False)

        self.apply_theme()

    def get_dark_theme_qss(self):
        return """
            QMainWindow, QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
            }
            QPushButton {
                background-color: #313244;
                border: none;
                padding: 10px;
                border-radius: 8px;
                color: #cdd6f4;
                font-size: 12px;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #45475a;
            }
            QPushButton:pressed {
                background-color: #585b70;
            }
            QPushButton:disabled {
                background-color: #6c7086;
                color: #9399b2;
            }
            QListWidget {
                background-color: #181825;
                border: none;
                border-radius: 8px;
                color: #cdd6f4;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QListWidget::item:alternate {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #181825;
                border: none;
                border-radius: 8px;
                padding: 5px;
                color: #cdd6f4;
            }
            QStatusBar {
                background-color: #181825;
                color: #cdd6f4;
                font-size: 10pt;
            }
            QMenu {
                background-color: #181825;
                border: none;
                color: #cdd6f4;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QLineEdit {
                background-color: #181825;
                border: none;
                border-radius: 8px;
                padding: 5px;
                color: #cdd6f4;
            }
        """

    def get_light_theme_qss(self):
        return """
            QMainWindow, QWidget {
                background-color: #f5f5f5;
                color: #1c2526;
            }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #d4d4d4;
                padding: 10px;
                border alkylborane: 8px;
                color: #1c2526;
                font-size: 12px;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border: 1px solid #0078d4;
            }
            QPushButton:pressed {
                background-color: #c7c7c7;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #a0a0a0;
            }
            QListWidget {
                background-color: #ffffff;
                border: 1px solid #d4d4d4;
                border-radius: 8px;
                color: #1c2526;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QListWidget::item:alternate {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #1c2526;
            }
            QSpinBox, QDoubleSpinBox {
                background-color: #ffffff;
                border: 1px solid #d4d4d4;
                border-radius: 8px;
                padding: 5px;
                color: #1c2526;
            }
            QStatusBar {
                background-color: #ffffff;
                color: #1c2526;
                font-size: 10pt;
            }
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d4d4d4;
                color: #1c2526;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d4d4d4;
                border-radius: 8px;
                padding: 5px;
                color: #1c2526;
            }
        """
    
    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet(self.get_dark_theme_qss())
            self.theme_button.setText("Light Mode")
            self.theme_button.setIcon(QIcon.fromTheme("weather-clear"))
        else:
            self.setStyleSheet(self.get_light_theme_qss())
            self.theme_button.setText("Dark Mode")
            self.theme_button.setIcon(QIcon.fromTheme("weather-clear-night"))

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
        self.last_action_time = time.time()
        
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)
       

        self.play_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.load_button.setEnabled(False)
        self.stop_playback_button.setEnabled(False)
        self.theme_button.setEnabled(False)
        self.inc_button.setEnabled(False)
        self.dec_button.setEnabled(False)
                
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
        self.inc_button.setEnabled(True)
        self.dec_button.setEnabled(True)
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
        self.inc_button.setEnabled(False)
        self.dec_button.setEnabled(False)
        
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
        self.inc_button.setEnabled(True)
        self.dec_button.setEnabled(True)
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
        delay_str = f"[Delay: {action.get('delay', 0.0):.2f}s]"
        if action['type'] == 'key_press':
            return f"{delay_str} Key Press: {action['key']}"
        elif action['type'] == 'mouse_click':
            btn_name = action['button'].replace('Button.', '').capitalize()
            return f"{delay_str} Mouse Click: ({action['x']}, {action['y']}) - {btn_name}"
        return f"{delay_str} Unknown Action"

    def populate_list_from_actions(self):
        self.action_list_widget.clear()
        for action in self.recorded_actions:
            action_text = self.format_action_to_string(action)
            self.action_list_widget.addItem(action_text)
            
    def show_context_menu(self, pos: QPoint):
        item = self.action_list_widget.itemAt(pos)
        if not item:
            return

        context_menu = QMenu(self)
        edit_action = QAction("Edit", self)
        edit_action.setIcon(QIcon.fromTheme("document-edit"))
        delete_action = QAction("Delete", self)
        delete_action.setIcon(QIcon.fromTheme("edit-delete"))
        
        context_menu.addAction(edit_action)
        context_menu.addAction(delete_action)
        
        action = context_menu.exec(self.action_list_widget.mapToGlobal(pos))
        
        if action == edit_action:
            self.edit_selected_action()
        elif action == delete_action:
            self.delete_selected_action()

    def edit_selected_action(self):
        selected_row = self.action_list_widget.currentRow()
        if selected_row < 0:
            return
            
        action_to_edit = self.recorded_actions[selected_row]
        
        dialog = EditActionDialog(action_to_edit, self)
        if dialog.exec():
            updated_action = dialog.get_data()
            self.recorded_actions[selected_row] = updated_action
            self.populate_list_from_actions()
            self.action_list_widget.setCurrentRow(selected_row)
            self.update_status("Action updated.")

    def delete_selected_action(self):
        selected_row = self.action_list_widget.currentRow()
        if selected_row < 0:
            return
            
        del self.recorded_actions[selected_row]
        self.populate_list_from_actions()
        self.update_status("Action deleted.")
        if not self.recorded_actions:
            self.play_button.setEnabled(False)
            self.save_button.setEnabled(False)
    
    def record_action(self, action_data):
        current_time = time.time()
        delay = current_time - self.last_action_time
        
        clamped_delay = 0.0
        if delay < 1.0:
            clamped_delay = 0.05
        elif delay > 30.0:
            clamped_delay = 30.0
        else:
            clamped_delay = delay
        
        if not self.recorded_actions:
            clamped_delay = 0.05

        action_data['delay'] = clamped_delay
        action_data['time'] = current_time
        
        self.recorded_actions.append(action_data)
        self.signals.action_added.emit(self.format_action_to_string(action_data))
        
        self.last_action_time = current_time

    def on_press(self, key):
        if self.is_recording:
            try:
                action = {'type': 'key_press', 'key': key.char}
            except AttributeError:
                action = {'type': 'key_press', 'key': str(key)}
            self.record_action(action)

    def on_click(self, x, y, button, pressed):
        if self.is_recording and pressed:
            action = {'type': 'mouse_click', 'x': x, 'y': y, 'button': str(button)}
            self.record_action(action)

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

                for index, action in enumerate(self.recorded_actions):
                    if self.stop_playback_flag:
                        break

                    delay = action.get('delay', 0.05)
                    time.sleep(delay)

                    self.signals.playback_highlight.emit(index)
                    
                    if self.stop_playback_flag:
                        break

                    if action['type'] == 'mouse_click':
                        mouse_ctrl.position = (action['x'], action['y'])
                        btn = mouse.Button.left if 'left' in action['button'] else mouse.Button.right if 'right' in action['button'] else mouse.Button.middle
                        mouse_ctrl.click(btn, 1)
                    
                    elif action['type'] == 'key_press':
                        key_to_press = action['key']
                        if isinstance(key_to_press, str) and key_to_press.startswith('Key.'):
                            key_name = key_to_press.split('.')[-1]
                            key_to_press = getattr(keyboard.Key, key_name, key_name)
                        
                        try:
                            keyboard_ctrl.press(key_to_press)
                            keyboard_ctrl.release(key_to_press)
                        except Exception as e:
                            print(f"Could not press key '{key_to_press}': {e}")
                
                if i < iterations - 1 and not self.stop_playback_flag:
                    time.sleep(1) 

        finally:
            self.signals.playback_finished.emit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutomatePro()
    window.show()
    sys.exit(app.exec())