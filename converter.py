import os
import sys
import platform
import subprocess
import threading
from tkinter import Tk, Label, Button, filedialog, messagebox
from tkinter.ttk import Progressbar
from PIL import Image, ExifTags, ImageTk
from tqdm import tqdm


# Global variables
MAX_WIDTH = 500
MAX_HEIGHT = 500

# Global variable to store the selected image path
selected_image_path = ""


def convert_image(image_path):
    try:
        # Open the selected image for preview
        preview_image = Image.open(image_path)
        preview_image.thumbnail((MAX_WIDTH, MAX_HEIGHT))

        # Display the preview image
        preview_photo = ImageTk.PhotoImage(preview_image)
        preview_label.config(image=preview_photo)
        preview_label.image = preview_photo

        # Get EXIF data
        exif_data = get_exif_data(image_path)
        exif_label.config(text=exif_data)

        # Convert image to BMP format
        basename = os.path.basename(image_path)
        bmp_path = os.path.splitext(basename)[0] + ".bmp"
        image = Image.open(image_path)
        image.save(bmp_path, "BMP")

        # Open the folder containing the converted image
        open_folder(os.path.dirname(image_path))

        # Display completion message
        status_label.config(text="Конвертация завершена!")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_label.config(text="Ошибка: " + str(e))
        print("Error:", str(e), file=sys.stderr)

    # Reset the selected image path and enable the Convert button
    selected_image_path = ""
    convert_button.config(state="normal")


def get_exif_data(image_path):
    exif_data = ""
    image = Image.open(image_path)

    if hasattr(image, "_getexif"):
        exif_info = image._getexif()

        if exif_info is not None:
            for tag, value in exif_info.items():
                if tag in ExifTags.TAGS:
                    tag_name = ExifTags.TAGS[tag]
                    exif_data += f"{tag_name}: {value}\n"

    return exif_data


def open_folder(folder_path):
    if platform.system() == "Windows":
        subprocess.Popen(["explorer", folder_path])
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", folder_path])
    else:
        try:
            subprocess.Popen(["xdg-open", folder_path])
        except FileNotFoundError:
            messagebox.showerror("Error", "Cannot open folder")
            status_label.config(text="Ошибка: Невозможно открыть папку")
            print("Error: Cannot open folder", file=sys.stderr)


def select_photo():
    filetypes = [("JPEG files", "*.jpg"), ("PNG files", "*.png")]
    image_path = filedialog.askopenfilename(filetypes=filetypes)

    if image_path:
        # Update the selected image path and enable the Convert button
        selected_image_path = image_path
        convert_button.config(state="normal")

        # Clear the preview and EXIF data labels
        preview_label.config(image="")
        exif_label.config(text="")


def convert_image_wrapper():
    if selected_image_path:
        convert_button.config(state="disabled")
        progress.start()

        # Start the conversion process in a separate thread
        threading.Thread(target=convert_image, args=(selected_image_path,)).start()


# Create UI window
window = Tk()
window.title("Конвертор1")

# Add label for status messages
status_label = Label(window, text="")
status_label.pack()

# Add label for image preview
preview_label = Label(window)
preview_label.pack()

# Add label for EXIF data
exif_label = Label(window, justify="left")
exif_label.pack()

# Add progress bar
progress = Progressbar(window, orient="horizontal", length=200, mode="determinate")
progress.pack()


# Add button to select photo
select_button = Button(window, text="Выбрать фото", command=select_photo)
select_button.pack()


# Add button to convert photo
convert_button = Button(window, text="Конвертировать", command=convert_image_wrapper)
convert_button.pack()
convert_button.config(state="disabled")  # Disable the button initially


# Add button to exit program
exit_button = Button(window, text="Выход", command=window.destroy)
exit_button.pack()


# Run the main UI loop
window.mainloop()


