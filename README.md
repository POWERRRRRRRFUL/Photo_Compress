以下是一个完整、简洁且专业的 `README.md` 文件示例，适用于你的 **Photo Compressor** 项目。此文件内容涵盖项目介绍、安装说明、使用步骤、依赖库，以及版权声明等。

```markdown
# Photo Compressor Application

A simple and user-friendly application to compress photos efficiently. The app provides a graphical interface with drag-and-drop support for ease of use, allowing users to specify a target size in MB for photo compression.

## Features

- **Drag-and-Drop Interface**: Easily drag and drop photos into the application for processing.
- **Custom Target Size**: Compress photos to a specified size in MB.
- **Progress Bar**: Visual progress indication during compression.
- **Batch Processing**: Compress multiple photos at once with ease.

## Requirements

Before running the application, ensure you have the following dependencies installed:

- **Python 3.x**
- **Pillow** (Image processing library)
- **TkinterDnD2** (For drag-and-drop functionality in the Tkinter GUI)
- **Tkinter** (For GUI functionality, comes pre-installed with Python on most platforms)

## Installation

Follow the steps below to set up and run the application:

### 1. Clone the Repository

```bash
git clone https://github.com/POWERRRRRRRFUL/Photo_Compress.git
cd Photo_Compress
```

### 2. Install Dependencies

To install the necessary Python libraries, run the following command:

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt` file, you can manually install the libraries using:

```bash
pip install Pillow
pip install tkinterdnd2
```

On **Linux** systems, you may need to install `tkinter` separately:

```bash
sudo apt-get install python3-tk
```

### 3. Running the Application

Once the dependencies are installed, you can start the application with:

```bash
python main.py
```

This will launch the photo compressor application with a graphical interface. Simply drag and drop images into the window and specify the target size in MB to begin compression.

## Usage

1. Open the application.
2. Drag and drop photos into the designated area.
3. Enter the target size (in MB) for the compressed photos.
4. Click the **Start Compression** button.
5. Monitor progress using the built-in progress bar.
6. Compressed photos will be saved in the same directory with a "_compressed" suffix in their filenames.

## Example

```plaintext
Original file: photo1.jpg (10 MB)
Target size: 2 MB
Result: photo1_compressed.jpg (1.9 MB)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## All Rights Reserved

All rights to this program are reserved. Unauthorized copying, distribution, modification, or any other usage of this software, in whole or in part, without the prior written permission of the author is strictly prohibited. For inquiries regarding commercial use or obtaining permission, please contact the author directly.
```
