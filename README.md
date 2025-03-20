# EXE Icon Changer

A professional GUI tool for changing, adding, and extracting icons from Windows executable files.

![EXE Icon Changer](bin/logo.png)

## 🚀 Features

- **User-friendly interface** for managing executable icons
- **Preview existing icons** in any executable file
- **Add or replace icons** from various image formats (PNG, JPG, ICO)
- **Extract icons** from executables to save for later use
- **Automatic backup** of original executables before modification
- **Image format conversion** (automatically converts any image to ICO format)

## 📋 Requirements

- Windows OS
- Python 3.6 or higher
- Dependencies listed below

## 📥 Installation

1. Clone this repository or download the ZIP file
```
git clone https://github.com/adithyanraj/exe-icon-changer.git
```

2. Install the required Python packages
```
pip install -r requirements.txt
```

3. Make sure ResourceHacker.exe is placed in the `bin` directory

## 🔧 Dependencies

```
pip install pyqt5 pillow pywin32
```

- PyQt5 - GUI framework
- Pillow (PIL) - Image processing
- PyWin32 - Windows API integration
- Resource Hacker (included in bin directory)

## 💻 Usage

1. Run the application
```
python exe-icon-changer.py
```

2. Select an EXE file using the "Browse" button
3. The application will display the current icons in the file
4. Select a new icon file using the second "Browse" button
5. Click "Add/Replace Icon" to update the executable
6. A backup of the original executable will be created automatically

## 🔍 Additional Options

- **Extract Icons**: Select an icon in the list and click "Extract Current Icon" to save it as an .ico file
- **Multiple Format Support**: You can use PNG, JPG or ICO files as new icons

## ⚠️ Important Notes

- The application creates a backup with the ".backup" extension before modifying any executable
- Administrative privileges may be required when modifying system executables
- Some executables with high security may not allow icon modifications

## 🛠️ Technical Details

The application uses:
- PyQt5 for the graphical interface
- Win32 API for icon extraction and handling
- Resource Hacker for resource modification
- PIL for image conversion and processing

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

- **Adithyanraj** - Initial work and maintenance

## 🙏 Acknowledgments

- [Resource Hacker](http://www.angusj.com/resourcehacker/) for providing the underlying resource editing functionality
