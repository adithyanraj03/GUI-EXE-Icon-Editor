import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, 
                            QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import win32api
import win32gui
import win32con
import win32ui
import struct
import tempfile
from PIL import Image

class ExeIconChanger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EXE Icon Changer - By Adithyanraj")
        self.setGeometry(300, 300, 800, 500)
        
        # Set application icon from the bin directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(script_dir, "bin", "logo.png")
        if os.path.exists(logo_path):
            app_icon = QIcon(logo_path)
            self.setWindowIcon(app_icon)
        
        # Initialize variables
        self.exe_path = None
        self.icon_path = None
        self.current_icons = []
        self.resource_hacker_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin", "ResourceHacker.exe")
        
        # Create main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create file selection area
        self.create_file_selection_area()
        
        # Create icon preview area
        self.create_icon_preview_area()
        
        # Create buttons area
        self.create_buttons_area()
        
        # Status message
        self.status_label = QLabel("Ready")
        self.main_layout.addWidget(self.status_label)

    def create_file_selection_area(self):
        # EXE file selection
        exe_layout = QHBoxLayout()
        self.exe_label = QLabel("Select EXE File:")
        self.exe_path_label = QLabel("No file selected")
        self.exe_browse_button = QPushButton("Browse")
        self.exe_browse_button.clicked.connect(self.browse_exe)
        
        exe_layout.addWidget(self.exe_label)
        exe_layout.addWidget(self.exe_path_label, 1)
        exe_layout.addWidget(self.exe_browse_button)
        
        # Icon file selection
        icon_layout = QHBoxLayout()
        self.icon_label = QLabel("Select Icon File:")
        self.icon_path_label = QLabel("No file selected")
        self.icon_browse_button = QPushButton("Browse")
        self.icon_browse_button.clicked.connect(self.browse_icon)
        
        icon_layout.addWidget(self.icon_label)
        icon_layout.addWidget(self.icon_path_label, 1)
        icon_layout.addWidget(self.icon_browse_button)
        
        # Add to main layout
        self.main_layout.addLayout(exe_layout)
        self.main_layout.addLayout(icon_layout)

    def create_icon_preview_area(self):
        preview_layout = QHBoxLayout()
        
        # Current icons
        current_layout = QVBoxLayout()
        current_label = QLabel("Current Icons:")
        self.current_icons_list = QListWidget()
        self.current_icons_list.setIconSize(QSize(48, 48))
        self.current_icons_list.setMaximumHeight(200)
        
        current_layout.addWidget(current_label)
        current_layout.addWidget(self.current_icons_list)
        
        # New icon
        new_layout = QVBoxLayout()
        new_label = QLabel("New Icon:")
        self.new_icon_preview = QLabel()
        self.new_icon_preview.setAlignment(Qt.AlignCenter)
        self.new_icon_preview.setMinimumSize(200, 200)
        self.new_icon_preview.setStyleSheet("border: 1px solid #cccccc;")
        
        new_layout.addWidget(new_label)
        new_layout.addWidget(self.new_icon_preview)
        
        # Add to preview layout
        preview_layout.addLayout(current_layout)
        preview_layout.addLayout(new_layout)
        
        # Add to main layout
        self.main_layout.addLayout(preview_layout)

    def create_buttons_area(self):
        buttons_layout = QHBoxLayout()
        
        self.add_icon_button = QPushButton("Add/Replace Icon")
        self.add_icon_button.clicked.connect(self.add_icon)
        self.add_icon_button.setEnabled(False)
        
        self.extract_icon_button = QPushButton("Extract Current Icon")
        self.extract_icon_button.clicked.connect(self.extract_icon)
        self.extract_icon_button.setEnabled(False)
        
        buttons_layout.addWidget(self.add_icon_button)
        buttons_layout.addWidget(self.extract_icon_button)
        
        self.main_layout.addLayout(buttons_layout)

    def browse_exe(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Executable", "", "Executable Files (*.exe)"
        )
        if file_path:
            self.exe_path = file_path
            self.exe_path_label.setText(file_path)
            self.status_label.setText("EXE file selected")
            self.extract_icon_button.setEnabled(True)
            self.load_current_icons()
            self.update_add_button_state()

    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Icon", "", "Icon Files (*.ico *.png *.jpg *.jpeg)"
        )
        if file_path:
            self.icon_path = file_path
            self.icon_path_label.setText(file_path)
            self.status_label.setText("Icon file selected")
            self.preview_new_icon()
            self.update_add_button_state()

    def update_add_button_state(self):
        # Convert to boolean to avoid passing None to setEnabled
        enabled = bool(self.exe_path and self.icon_path)
        self.add_icon_button.setEnabled(enabled)

    def load_current_icons(self):
        self.current_icons_list.clear()
        self.current_icons = []
        
        try:
            # Extract icons from the executable
            large_icons, small_icons = win32gui.ExtractIconEx(self.exe_path, -1)
            
            # Close the small icon handles
            for small_icon in small_icons:
                win32gui.DestroyIcon(small_icon)
            
            # Add the large icons to the list and keep their handles
            for i, icon_handle in enumerate(large_icons):
                # Create a temporary icon file
                temp_path = os.path.join(tempfile.gettempdir(), f"temp_icon_{i}.ico")
                self.save_icon_to_file(icon_handle, temp_path)
                
                # Create a QIcon and add it to the list
                pixmap = QPixmap(temp_path)
                item = QListWidgetItem(QIcon(pixmap), f"Icon {i}")
                self.current_icons_list.addItem(item)
                
                # Store the icon information
                self.current_icons.append({
                    'handle': icon_handle,
                    'temp_path': temp_path,
                    'index': i
                })
            
            if not large_icons:
                item = QListWidgetItem("No icons found")
                self.current_icons_list.addItem(item)
                
        except Exception as e:
            self.status_label.setText(f"Error loading icons: {str(e)}")
            item = QListWidgetItem("Error loading icons / Exe has no icons")
            self.current_icons_list.addItem(item)

    def save_icon_to_file(self, icon_handle, file_path):
        # Get the icon info
        icon_info = win32gui.GetIconInfo(icon_handle)
        hbmColor = icon_info[4]
        
        # Create a device context
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)
        hdc.DrawIcon((0, 0), icon_handle)
        
        # Save the bitmap to a temporary file
        hbmp.SaveBitmapFile(hdc, file_path)
        
        # Clean up
        win32gui.DeleteObject(hbmColor)
        hdc.DeleteDC()

    def preview_new_icon(self):
        if self.icon_path and os.path.exists(self.icon_path):
            pixmap = QPixmap(self.icon_path)
            scaled_pixmap = pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.new_icon_preview.setPixmap(scaled_pixmap)
            self.status_label.setText("New icon preview loaded")
        else:
            self.new_icon_preview.clear()
            self.status_label.setText("Failed to load icon preview")

    def add_icon(self):
        if not self.exe_path or not self.icon_path:
            self.status_label.setText("Please select both an EXE file and an icon file")
            return
            
        try:
            # Convert the icon if it's not an ICO file
            icon_path = self.icon_path
            if not icon_path.lower().endswith('.ico'):
                icon_path = self.convert_to_ico(self.icon_path)
                if not icon_path:
                    self.status_label.setText("Failed to convert icon format")
                    return
            
            # Use resource editor to change the icon
            import subprocess
            import platform
            
            # First, make a backup of the original exe
            backup_path = f"{self.exe_path}.backup"
            if not os.path.exists(backup_path):
                import shutil
                shutil.copy2(self.exe_path, backup_path)
                
            # Use ResourceHacker to change the icon
            resource_hacker_path = self.resource_hacker_path  # Use the path from bin directory
            
            # Check if ResourceHacker exists
            if not self.check_resource_hacker():
                return
                
            # Command to change the icon
            cmd = [
                resource_hacker_path,
                "-open", self.exe_path,
                "-save", self.exe_path,
                "-action", "addoverwrite",
                "-res", icon_path,
                "-mask", "ICONGROUP,MAINICON,"
            ]
            
            process = subprocess.Popen(cmd, 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
            stdout, stderr = process.communicate()
            
            if process.returncode == 0:
                self.status_label.setText("Icon successfully changed!")
                self.load_current_icons()  # Reload the icons
                QMessageBox.information(self, "Success", 
                                       "Icon has been changed successfully!\n"
                                       f"A backup of the original file was saved to {backup_path}")
            else:
                error_msg = stderr.decode() if stderr else "Unknown error"
                self.status_label.setText(f"Error changing icon: {error_msg}")
                QMessageBox.warning(self, "Error", 
                                   f"Failed to change the icon. Error: {error_msg}")
                
        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def check_resource_hacker(self):
        # Check if ResourceHacker is available in the bin directory
        if os.path.exists(self.resource_hacker_path):
            return True
        else:
            QMessageBox.warning(
                self, 
                "Resource Hacker Not Found", 
                f"ResourceHacker.exe was not found at:\n{self.resource_hacker_path}\n\n"
                "Please make sure ResourceHacker.exe is in the 'bin' directory."
            )
            self.status_label.setText("Resource Hacker not found in the bin directory")
            return False

    def convert_to_ico(self, image_path):
        try:
            # Create a temporary ICO file
            temp_ico = os.path.join(tempfile.gettempdir(), "temp_icon.ico")
            
            # Use PIL to convert the image to ICO
            img = Image.open(image_path)
            
            # Prepare sizes for the icon (Windows standard sizes)
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            
            # Create images for each size
            img_list = []
            for size in sizes:
                resized_img = img.resize(size, Image.LANCZOS)
                img_list.append(resized_img)
                
            # Save as ICO
            img_list[0].save(
                temp_ico, 
                format='ICO', 
                sizes=[(img.width, img.height) for img in img_list]
            )
            
            return temp_ico
        except Exception as e:
            self.status_label.setText(f"Error converting image: {str(e)}")
            return None

    def extract_icon(self):
        if not self.exe_path:
            self.status_label.setText("Please select an EXE file first")
            return
            
        # If no icons were found, show a message
        if not self.current_icons:
            QMessageBox.information(self, "No Icons", "No icons were found in the selected executable.")
            return
            
        # Get the selected icon or the first one if none selected
        selected_items = self.current_icons_list.selectedItems()
        if selected_items:
            selected_index = self.current_icons_list.row(selected_items[0])
        else:
            selected_index = 0
            
        if selected_index >= len(self.current_icons):
            self.status_label.setText("Invalid icon selection")
            return
            
        # Ask where to save the icon
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Icon", "", "Icon Files (*.ico)"
        )
        
        if not save_path:
            return
            
        if not save_path.lower().endswith('.ico'):
            save_path += '.ico'
            
        # Copy the temporary icon file to the save location
        try:
            import shutil
            temp_path = self.current_icons[selected_index]['temp_path']
            shutil.copy2(temp_path, save_path)
            self.status_label.setText(f"Icon saved to {save_path}")
            QMessageBox.information(self, "Success", f"Icon has been saved to {save_path}")
        except Exception as e:
            self.status_label.setText(f"Error saving icon: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to save the icon. Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExeIconChanger()
    window.show()
    sys.exit(app.exec_())
