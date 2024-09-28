import os
import threading
from tkinter import Tk, Frame, Button, messagebox, filedialog, Menu, Canvas, Scrollbar, VERTICAL, RIGHT, Y
from tkinter.ttk import Progressbar, Entry, Label, Style
from PIL import Image, ImageTk, ImageEnhance
from tkinterdnd2 import TkinterDnD, DND_FILES
import time


# 版权信息
def show_copyright():
    messagebox.showinfo("Copyright", "版权所有：Zhou Jingsong\n版本: 1.0\n作者：Zhou Jingsong\n")


# 隐私条款
def show_privacy_policy():
    messagebox.showinfo("隐私条款", "本软件不收集任何个人数据。所有图片均只在本地处理。")


# 压缩图片（添加优化参数并改进进度条更新）
def compress_image(file_path, target_size_mb, progress_callback):
    target_size_bytes = target_size_mb * 1024 * 1024
    current_size = os.path.getsize(file_path)

    if current_size <= target_size_bytes:
        return file_path, "No compression needed"

    with Image.open(file_path) as img:
        file_name, file_extension = os.path.splitext(file_path)
        compressed_file_path = f"{file_name}_compressed{file_extension}"
        quality = 95
        step = 1
        last_valid_size = current_size

        # 每次压缩尝试时更新进度
        while True:
            quality = max(1, min(95, quality))
            img.save(compressed_file_path, quality=quality, subsampling=0, optimize=True)  # 优化压缩参数
            compressed_size = os.path.getsize(compressed_file_path)

            # 更新进度条以显示压缩过程
            progress_callback(5)  # 每次循环增加5%的进度

            if target_size_bytes * 0.95 <= compressed_size <= target_size_bytes:
                last_valid_size = compressed_size
                break

            if compressed_size < target_size_bytes and compressed_size > last_valid_size:
                break

            if compressed_size > target_size_bytes:
                last_valid_size = compressed_size
                quality -= step
            else:
                break

    return compressed_file_path, f"Compressed to {last_valid_size / (1024 * 1024):.2f} MB"


# 使用多线程并行压缩文件并改进进度条更新
def process_files_in_parallel(file_paths, target_size_mb):
    progress_bar['value'] = 0
    total_files = len(file_paths)
    increment_per_file = 100 / total_files

    def compress_single_file(file_path, idx):
        progress = 0

        # 定义进度更新回调函数
        def update_progress(increment):
            nonlocal progress
            progress += increment
            progress_bar['value'] = min(progress_bar['value'] + increment, 100)
            root.update_idletasks()
            time.sleep(0.01)  # 模拟更平滑的动画效果

        compressed_path, message = compress_image(file_path, target_size_mb, update_progress)
        progress_label.config(text=f"Processed {os.path.basename(compressed_path)}: {message}")

        # 将文件完成进度加到总进度条中
        progress_bar['value'] = min(progress_bar['value'] + increment_per_file, 100)
        root.update_idletasks()

    threads = []
    for idx, file_path in enumerate(file_paths):
        thread = threading.Thread(target=compress_single_file, args=(file_path, idx))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    messagebox.showinfo("Compression Completed", "All selected images have been processed.")
    progress_label.config(text="Ready for next batch")
    reset_interface()


# 选择文件（通过对话框）
def select_files():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif;*.tiff")]
    )
    add_files(files)


# 拖放文件到窗口
def drop(event):
    files = root.tk.splitlist(event.data)
    add_files(files)


# 添加文件并生成预览
def add_files(files):
    for file in files:
        if file not in file_paths:
            file_paths.append(file)
            selected_files.append(False)  # 初始未选中
            add_file_preview(file)

            # 检查文件格式，并根据格式给出提示
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension == ".bmp":
                messagebox.showinfo("注意", "BMP文件是无压缩格式，可能不会有很好的压缩效果。")
            elif file_extension == ".gif":
                messagebox.showinfo("注意", "GIF文件是固定的压缩格式，可能不会支持质量压缩，且动画GIF会丢失动画。")
            elif file_extension == ".tiff":
                messagebox.showinfo("注意", "TIFF文件可能是多页格式，请确保您想要压缩的图像是单页。")


# 生成并显示文件的预览
def add_file_preview(file_path):
    with Image.open(file_path) as img:
        img.thumbnail((100, 100))  # 生成缩略图
        img_tk = ImageTk.PhotoImage(img)

    x_offset = len(preview_images) * 110
    img_id = preview_canvas.create_image(x_offset, 10, anchor='nw', image=img_tk)
    preview_canvas.image_list.append(img_tk)  # 保存引用以防止图片被垃圾回收
    preview_images.append(img_id)

    # 绑定点击事件
    preview_canvas.tag_bind(img_id, '<Button-1>', lambda e, idx=len(preview_images) - 1: toggle_selection(idx))


# 切换选择状态
def toggle_selection(index):
    selected_files[index] = not selected_files[index]
    redraw_previews()


# 重绘所有预览，应用选中状态
def redraw_previews():
    preview_canvas.delete("all")
    preview_canvas.image_list.clear()
    preview_images.clear()
    for idx, file_path in enumerate(file_paths):
        with Image.open(file_path) as img:
            img.thumbnail((100, 100))  # 生成缩略图
            if selected_files[idx]:
                img = ImageEnhance.Brightness(img).enhance(0.5)  # 选中后变灰
            img_tk = ImageTk.PhotoImage(img)

        x_offset = idx * 110
        img_id = preview_canvas.create_image(x_offset, 10, anchor='nw', image=img_tk)
        preview_canvas.image_list.append(img_tk)
        preview_images.append(img_id)

        # 绑定点击事件
        preview_canvas.tag_bind(img_id, '<Button-1>', lambda e, idx=idx: toggle_selection(idx))


# 删除选中的文件
def delete_selected_files():
    global file_paths, selected_files
    new_file_paths = []
    new_selected_files = []
    preview_canvas.delete("all")
    preview_canvas.image_list.clear()
    preview_images.clear()
    for i in range(len(file_paths)):
        if not selected_files[i]:  # 如果未被选中，保留文件
            new_file_paths.append(file_paths[i])
            new_selected_files.append(False)

    file_paths = new_file_paths
    selected_files = new_selected_files
    redraw_previews()


# 开始压缩
def start_compression():
    if not file_paths:
        messagebox.showwarning("No Files", "Please select images to compress.")
        return

    target_size = target_size_entry.get()
    try:
        target_size_mb = round(float(target_size))  # Ensure the input is rounded to nearest integer
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the target size.")
        return

    # 使用多线程并行压缩文件
    compression_thread = threading.Thread(target=process_files_in_parallel, args=(file_paths, target_size_mb))
    compression_thread.start()


# 重置界面
def reset_interface():
    global file_paths, selected_files
    file_paths = []
    selected_files = []
    preview_canvas.delete("all")
    preview_canvas.image_list.clear()
    preview_images.clear()
    progress_label.config(text="Ready to process files")
    progress_bar['value'] = 0


# 主窗口创建
root = TkinterDnD.Tk()
root.title("Photo Compressor")
root.geometry("800x600")  # Set default window size to 800x600
root.minsize(800, 600)  # Prevent window from being smaller than 800x600
root.configure(bg='#F2F2F2')  # Light gray background color

# 菜单栏
menu_bar = Menu(root)
root.config(menu=menu_bar)
help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Privacy Policy", command=show_privacy_policy)
help_menu.add_command(label="Copyright", command=show_copyright)

# 样式设置
style = Style()
style.configure("TButton", font=("Helvetica", 10), padding=5)
style.configure("TLabel", font=("Helvetica", 10), background="#F2F2F2", foreground="#333333")
style.configure("TEntry", font=("Helvetica", 10), padding=5)
style.configure("TProgressbar", thickness=15)

# 目标大小
Label(root, text="Select photos and set the target size (MB):").pack(pady=8)
frame = Frame(root, bg='#F2F2F2')
frame.pack(pady=5)
Label(frame, text="Target Size (MB):").grid(row=0, column=0)
target_size_entry = Entry(frame, font=("Helvetica", 10))
target_size_entry.grid(row=0, column=1)

# 提示文字
Label(root,
      text="Drag and drop images here or use 'Select Files' button. Click on thumbnails to select/deselect.").pack(
    pady=5)

# 文件预览区域
preview_frame = Frame(root, bg='#FFFFFF')
preview_frame.pack(pady=8, fill="both", expand=True)
preview_canvas = Canvas(preview_frame, bg='#FFFFFF', scrollregion=(0, 0, 1000, 200))  # 设置滚动区域
preview_canvas.pack(side='left', fill='both', expand=True)
preview_canvas.image_list = []  # 保存所有预览的引用，防止被垃圾回收
preview_images = []  # 保存所有图片的ID，用于重绘

scrollbar = Scrollbar(preview_frame, orient=VERTICAL, command=preview_canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
preview_canvas.config(yscrollcommand=scrollbar.set)

# 进度条
progress_bar = Progressbar(root, length=400, mode='determinate')
progress_bar.pack(pady=8)
progress_label = Label(root, text="Ready to process files")
progress_label.pack(pady=5)

# 文件选择按钮
select_button = Button(root, text="Select Files", command=select_files, font=("Helvetica", 10, "normal"))
select_button.pack(pady=5)

# 删除选择的文件按钮
delete_button = Button(root, text="Delete Selected Files", command=delete_selected_files,
                       font=("Helvetica", 10, "normal"))
delete_button.pack(pady=5)

# 开始压缩按钮
start_button = Button(root, text="Start Compression", command=start_compression, font=("Helvetica", 10, "normal"))
start_button.pack(pady=5)

# 重置按钮
reset_button = Button(root, text="Reset", command=reset_interface, font=("Helvetica", 10, "normal"))
reset_button.pack(pady=5)

# 注册拖放事件
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

# 初始化文件列表
file_paths = []
selected_files = []

root.mainloop()
