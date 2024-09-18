import os
import threading
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, Text
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.ttk import Progressbar
from PIL import Image


def compress_image(file_path, target_size_mb):
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

        while True:
            quality = max(1, min(95, quality))
            img.save(compressed_file_path, quality=quality, subsampling=0)
            compressed_size = os.path.getsize(compressed_file_path)

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


def process_files(file_paths, target_size_mb):
    progress_bar['value'] = 0
    total_files = len(file_paths)

    for idx, file_path in enumerate(file_paths):
        compressed_path, message = compress_image(file_path, target_size_mb)
        progress_label.config(text=f"Processed {os.path.basename(compressed_path)}: {message}")
        progress_bar['value'] = (idx + 1) / total_files * 100
        root.update_idletasks()

    messagebox.showinfo("Compression Completed", "All selected images have been processed.")

    # Add a separator line after each batch processing
    file_list.config(state="normal")
    file_list.insert("end", "\n" + "=" * 50 + "\n")  # Add a separator line to distinguish batches
    file_list.config(state="disabled")

    # Update the status and allow for next batch processing
    progress_label.config(text="Ready for next batch")
    reset_interface()


def drop(event):
    files = root.tk.splitlist(event.data)
    file_paths.extend(files)
    file_list.config(state="normal")
    file_list.delete(1.0, "end")
    file_list.insert("end", "\n".join(file_paths) + "\n")
    file_list.config(state="disabled")


def start_compression():
    if not file_paths:
        messagebox.showwarning("No Files", "Please drag and drop images to compress.")
        return

    target_size = target_size_entry.get()
    try:
        target_size_mb = round(float(target_size))  # Ensure the input is rounded to nearest integer
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the target size.")
        return

    # Run compression in a background thread to keep GUI responsive
    compression_thread = threading.Thread(target=process_files, args=(file_paths, target_size_mb))
    compression_thread.start()


def reset_interface():
    """Reset the interface to prepare for a new batch of files."""
    global file_paths
    file_paths = []  # Clear the file list
    file_list.config(state="normal")
    file_list.delete(1.0, "end")  # Clear the text area
    file_list.config(state="disabled")
    progress_label.config(text="Ready to process files")
    progress_bar['value'] = 0


# Create main window
root = TkinterDnD.Tk()
root.title("Photo Compressor")
root.geometry("600x450")

# Instructions label
Label(root, text="Drag and drop photos below and set the target size (MB):").pack(pady=10)

# Entry for target size
frame = Frame(root)
frame.pack(pady=10)
Label(frame, text="Target Size (MB):").grid(row=0, column=0)
target_size_entry = Entry(frame)
target_size_entry.grid(row=0, column=1)

# Text area to show dropped files
file_paths = []
file_list = Text(root, width=70, height=10, bg="white", state="disabled")
file_list.pack(pady=10)
file_list.drop_target_register(DND_FILES)
file_list.dnd_bind('<<Drop>>', drop)

# Progress bar
progress_bar = Progressbar(root, length=500, mode='determinate')
progress_bar.pack(pady=10)
progress_label = Label(root, text="Ready to process files")
progress_label.pack(pady=5)

# Start compression button
start_button = Button(root, text="Start Compression", command=start_compression)
start_button.pack(pady=5)

# Reset button to prepare for a new batch of files
reset_button = Button(root, text="Reset", command=reset_interface)
reset_button.pack(pady=5)

root.mainloop()
