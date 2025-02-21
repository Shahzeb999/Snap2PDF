# Zoom Snap

A lightweight screenshot tool designed for capturing and compiling meeting screenshots into PDF documents. Perfect for taking notes during Zoom meetings or any other screen-sharing sessions.

## Features

- Floating, draggable window that stays on top
- One-click screenshot capture
- Automatic PDF compilation
- Automatic cleanup of individual screenshots after PDF creation
- Timestamps for all captures
- Easy access to save location
- Minimal system resource usage

## Requirements

- Python 3.x
- Required Python packages:
  ```
  Pillow>=10.0.0
  reportlab>=4.0.0
  ```

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. If you're on Linux, you might need to install tkinter:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # Fedora
   sudo dnf install python3-tkinter
   
   # Arch Linux
   sudo pacman -S tk
   ```

## Usage

1. Run the script:
   ```bash
   python project.py
   ```

2. The Zoom Snap window will appear in the top-right corner of your screen

3. Interface buttons:
   - 📸 Capture: Takes a screenshot
   - 💾 Save PDF: Compiles all screenshots into a PDF and cleans up
   - 📁 Folder: Opens the save location
   - ✕ Close: Exits the application

4. Screenshots and PDFs are saved in the `Screenshots` folder in the same directory as the script

## How it Works

1. When you click "Capture":
   - The tool window temporarily hides itself
   - Takes a screenshot of your entire screen
   - Saves it with a timestamp
   - Shows you how many screenshots you've taken

2. When you click "Save PDF":
   - All screenshots are compiled into a single PDF
   - Individual screenshot files are automatically deleted
   - The save folder opens automatically
   - The PDF is named with the current timestamp

## File Structure

```
project_directory/
│
├── project.py         # Main application script
├── requirements.txt   # Required Python packages
├── README.md         # This file
│
└── Screenshots/      # Created automatically
    └── meeting_notes_[timestamp].pdf  # Your saved PDFs
```

## Troubleshooting

1. **Window won't stay on top**: Make sure no other applications are forcing themselves to be topmost
2. **Capture button not working**: Check if your system allows the application to capture screenshots
3. **PDF saving error**: Ensure you have write permissions in the Screenshots directory

## Contributing

Feel free to fork this project and submit pull requests for any improvements you make.

## License

This project is released under the MIT License. Feel free to use it for any purpose.

## Known Issues

- The window might flicker briefly when taking screenshots
- On some systems, the PDF compilation might take a few seconds for many screenshots
