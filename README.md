"""
# Photo Compressor Application

This simple program is designed to compress photos easily with a user-friendly GUI. The application allows users to drag and drop images into the interface and compress them to a specified size.

## Requirements

To run this application, you need the following libraries:

1. **Pillow**: Used for image processing and compression.
2. **TkinterDnD2**: Used to enable drag-and-drop support in the tkinter GUI.
3. **Tkinter**: The standard Python GUI toolkit. For Linux users, this may need to be installed separately.

## Installation

Follow these steps to set up and run the application:

### 1. Clone the repository:
```bash
git clone https://github.com/POWERRRRRRRFUL/Photo_Compress.git
cd Photo_Compress
2. Install dependencies:
bash
复制代码
pip install -r requirements.txt
If requirements.txt is not available, manually install the dependencies:

bash
复制代码
pip install Pillow
pip install tkinterdnd2
For Linux users, you may need to install tkinter using the package manager:

bash
复制代码
sudo apt-get install python3-tk
Running the Application
Once all dependencies are installed, you can run the application by executing the following command:

bash
复制代码
python main.py
The GUI will open, allowing you to drag and drop images and specify the target compression size (in MB).

Main Features
Drag and Drop Support: Users can drag and drop photos directly into the application.
Image Compression: Compresses photos to a user-defined target size (in MB).
Progress Bar: Displays the compression progress for multiple images.
Batch Processing: Multiple images can be processed in one batch.
All Rights Reserved
All rights to this program are reserved. Unauthorized copying, distribution, modification, or any other usage of this software, in whole or in part, without the prior written permission of the author is strictly prohibited. For inquiries regarding commercial use or obtaining permission, please contact the author directly.

"""

markdown
复制代码

### 文件结构说明：

- **Program Introduction**: 简要介绍程序的功能。
- **Requirements**: 列出运行该程序所需的库，包括 `Pillow` 和 `TkinterDnD2`，并说明 `Tkinter` 的安装情况，尤其是在 Linux 上。
- **Installation**: 提供克隆 GitHub 仓库和安装依赖库的说明。
- **Running the Application**: 说明如何运行应用程序并启动 GUI。
- **Main Features**: 列出应用程序的主要功能，如拖放支持、图像压缩、进度条等。
- **All Rights Reserved**: 包含版权声明，明确未经许可禁止使用或修改。

### 依赖安装提示：

在 `requirements.txt` 中应包含：

Pillow==9.1.0 tkinterdnd2==0.3.0
