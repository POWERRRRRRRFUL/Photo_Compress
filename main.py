import os
import threading
from tkinter import Tk, Text, Entry, Frame, Button, messagebox  # Use tkinter.Button and messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter.ttk import Progressbar, Label, Style
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
root.geometry("500x400")  # Set default window size to 500x400
root.minsize(500, 400)  # Prevent window from being smaller than 500x400
root.configure(bg='#F2F2F2')  # Light gray background color

# Improve DPI awareness for high-resolution displays
root.tk.call('tk', 'scaling', 1.5)  # Set DPI scaling to 150%

# Style for Apple-like appearance
style = Style()
style.configure("TButton", font=("Helvetica", 12), padding=5)  # Adjust button font size and padding
style.configure("TLabel", font=("Helvetica", 10), background="#F2F2F2", foreground="#333333")  # Smaller font size
style.configure("TEntry", font=("Helvetica", 10), padding=5)
style.configure("TProgressbar", thickness=15)  # Thinner progress bar

# Instructions label
Label(root, text="Drag and drop photos below and set the target size (MB):", style="TLabel").pack(pady=8)

# Entry for target size
frame = Frame(root, bg='#F2F2F2')  # Using tkinter Frame to allow background color
frame.pack(pady=5)
Label(frame, text="Target Size (MB):", style="TLabel").grid(row=0, column=0)
target_size_entry = Entry(frame, font=("Helvetica", 10), relief="flat", bg="#FFFFFF", highlightthickness=0)
target_size_entry.grid(row=0, column=1)

# Text area to show dropped files
file_paths = []
file_list = Text(root, width=60, height=8, bg="#FFFFFF", state="disabled", font=("Helvetica", 10), relief="flat",
                 highlightthickness=0)
file_list.pack(pady=8)
file_list.drop_target_register(DND_FILES)
file_list.dnd_bind('<<Drop>>', drop)

# Progress bar
progress_bar = Progressbar(root, length=400, mode='determinate')  # Adjust progress bar length
progress_bar.pack(pady=8)
progress_label = Label(root, text="Ready to process files", style="TLabel")
progress_label.pack(pady=5)

# Start compression button with Apple-like design
start_button = Button(root, text="Start Compression", command=start_compression, font=("Helvetica", 12, "normal"),
                      bg="#E8E8E8", activebackground="#D0D0D0", relief="flat", borderwidth=2, padx=20, pady=8,
                      highlightthickness=2, highlightbackground="#C0C0C0")
start_button.pack(pady=5)

# Reset button with Apple-like design
reset_button = Button(root, text="Reset", command=reset_interface, font=("Helvetica", 12, "normal"),
                      bg="#E8E8E8", activebackground="#D0D0D0", relief="flat", borderwidth=2, padx=20, pady=8,
                      highlightthickness=2, highlightbackground="#C0C0C0")
reset_button.pack(pady=5)

root.mainloop()
