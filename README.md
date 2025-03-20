# EXE Icon Changer

A professional GUI tool for changing, adding, and extracting icons from Windows executable files.

![image](https://github.com/user-attachments/assets/860fd7fc-abff-442d-ae6c-b24ef65abad7)

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

Clone this repository or download the ZIP file
```
git clone https://github.com/adithyanraj/exe-icon-changer.git
```

## 🔧 Dependencies

```
pip install pyqt5 pillow pywin32
```
or On Linux
```
pip3 install pyqt5 pillow pywin32
```

- PyQt5 - GUI framework
- Pillow (PIL) - Image processing
- PyWin32 - Windows API integration

## 💻 Usage

1. Run the application
```
python Main.py
```
or On Linux

```
python3 Main.py
```
![image](https://github.com/user-attachments/assets/6b14b971-be31-43dd-a096-900c8b7238e5)

2. Select an EXE file using the "Browse" button
![image](https://github.com/user-attachments/assets/21edaddb-2268-4a38-ab3c-8655b3c36c61)

3. The application will display the current icons in the file
4. Select a new icon file using the second "Browse" button
5. Click "Add/Replace Icon" to update the executable
![image](https://github.com/user-attachments/assets/c5284122-ac37-4ecb-ad92-57c34a9fca2d)

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

This project is licensed under the MIT License - see the [LICENSE](https://github.com/adithyanraj03/GUI-EXE-Icon-Editor/blob/main/LICENSE) file for details.


## Contact

For questions or feedback, feel free to reach out 😄 click: [Email](https://mail.google.com/mail/?view=cm&fs=1&to=adithyanraj03@gmail.com&su=EXE%20Icon%20Changer&body=Hello%20Developer%20Adithya,%0A%0AI%20came%20across%20your%20Git%20repository%20for%20the%20EXE%20Icon%20Changer%20and%20wanted%20to%20reach%20out.%0A%0AI'm%20interested%20in%20discussing%20some%20ideas.%0A%0ABest,%0A[Your%20Name]
)

## 👨‍💻 Author

- **Adithyanraj**

## 🙏 Acknowledgments

- [Resource Hacker](http://www.angusj.com/resourcehacker/) for providing the underlying resource editing functionality
