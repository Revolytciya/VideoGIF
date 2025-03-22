import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import numpy as np
import os
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class NoiseGIFGenerator:
    def __init__(self, width, height, frames, duration, pixel_size, output_path):
        self.width = width
        self.height = height
        self.frames = frames
        self.duration = duration
        self.pixel_size = pixel_size
        self.output_path = output_path

    def create_noise_frame(self, index):
        """Создает случайный цветной пиксельный кадр."""
        try:
            img = np.random.randint(0, 256, (self.height, self.width, 3), dtype=np.uint8)

            if self.pixel_size > 1:
                img = img[::self.pixel_size, ::self.pixel_size]
                img = np.repeat(np.repeat(img, self.pixel_size, axis=0), self.pixel_size, axis=1)

            return Image.fromarray(img)
        except Exception as e:
            logging.error(f"Ошибка при создании кадра {index}: {e}")
            return None

    def create_gif(self, progress_callback):
        """Генерирует и сохраняет GIF-анимацию."""
        try:
            frames = [self.create_noise_frame(i) for i in range(self.frames)]
            frames = [frame for frame in frames if frame]

            if not frames:
                raise ValueError("Не удалось создать кадры GIF.")

            frames[0].save(
                self.output_path,
                save_all=True,
                append_images=frames[1:],
                duration=self.duration,
                loop=0
            )
            logging.info(f"GIF сохранен: {self.output_path}")
            return self.output_path
        except Exception as e:
            logging.error(f"Ошибка при создании GIF: {e}")
            return None


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("GIFHD Generator")
        self.root.geometry("350x500")

        self.save_path = tk.StringVar()
        self.filename_var = tk.StringVar(value="GIFHD")
        self.resolution_var = tk.StringVar(value="1920x1080")
        self.frames_var = tk.IntVar(value=30)
        self.duration_var = tk.IntVar(value=100)
        self.pixel_size_var = tk.IntVar(value=10)

        self.setup_ui()

    def setup_ui(self):
        """Настраивает элементы интерфейса."""
        tk.Label(self.root, text="Выберите разрешение:").pack()
        self.resolution_menu = ttk.Combobox(
            self.root,
            values=[
                "1920x1080", "1080x1920", "2560x1440", "1440x2560", "3840x2160", "2160x3840", "Другое"
            ],
            textvariable=self.resolution_var,
            state="readonly"
        )
        self.resolution_menu.pack()
        self.resolution_menu.bind("<<ComboboxSelected>>", self.toggle_custom_resolution)

        self.custom_resolution_frame = tk.Frame(self.root)
        tk.Label(self.custom_resolution_frame, text="Ширина:").pack(side=tk.LEFT)
        self.custom_width_var = tk.StringVar()
        tk.Entry(self.custom_resolution_frame, textvariable=self.custom_width_var, width=6).pack(side=tk.LEFT)
        tk.Label(self.custom_resolution_frame, text="Высота:").pack(side=tk.LEFT)
        self.custom_height_var = tk.StringVar()
        tk.Entry(self.custom_resolution_frame, textvariable=self.custom_height_var, width=6).pack(side=tk.LEFT)

        tk.Label(self.root, text="Размер пикселя (1-100):").pack()
        tk.Scale(self.root, from_=1, to=100, orient="horizontal", variable=self.pixel_size_var, length=250).pack()

        tk.Label(self.root, text="Число кадров:").pack()
        tk.Scale(self.root, from_=10, to=300, orient="horizontal", variable=self.frames_var, length=250).pack()

        tk.Label(self.root, text="Длительность кадра (мс):").pack()
        tk.Scale(self.root, from_=10, to=500, orient="horizontal", variable=self.duration_var, length=250).pack()

        tk.Label(self.root, text="Имя файла:").pack()
        tk.Entry(self.root, textvariable=self.filename_var).pack()

        self.path_button = tk.Button(self.root, text="Выбрать папку", command=self.choose_save_path)
        self.path_button.pack()
        tk.Label(self.root, textvariable=self.save_path, fg="blue").pack()

        self.progress = ttk.Progressbar(self.root, length=250, mode='determinate')
        self.progress.pack()

        self.create_button = tk.Button(self.root, text="Создать GIF", command=self.start_generation)
        self.create_button.pack()

    def toggle_custom_resolution(self, event=None):
        """Переключает кастомное разрешение."""
        if self.resolution_var.get() == "Другое":
            self.custom_resolution_frame.pack()
        else:
            self.custom_resolution_frame.pack_forget()

    def choose_save_path(self):
        """Выбирает папку сохранения."""
        folder = filedialog.askdirectory()
        if folder:
            self.save_path.set(folder)

    def get_settings(self):
        """Получает настройки GIF."""
        if self.resolution_var.get() == "Другое":
            try:
                width = int(self.custom_width_var.get())
                height = int(self.custom_height_var.get())
                if width <= 0 or height <= 0:
                    raise ValueError("Неверные размеры!")
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные размеры!")
                return None
        else:
            width, height = map(int, self.resolution_var.get().split("x"))

        frames = self.frames_var.get()
        duration = self.duration_var.get()
        pixel_size = self.pixel_size_var.get()

        return width, height, frames, duration, pixel_size

    def start_generation(self):
        """Запускает генерацию GIF."""
        settings = self.get_settings()
        if not settings:
            return

        width, height, frames, duration, pixel_size = settings
        output_folder = self.save_path.get()
        filename = self.filename_var.get().strip()

        if not output_folder:
            messagebox.showerror("Ошибка", "Выберите папку для сохранения!")
            return
        if not filename:
            messagebox.showerror("Ошибка", "Введите имя файла!")
            return

        output_path = os.path.join(output_folder, f"{filename}.gif")
        self.create_button.config(state='disabled')

        generator = NoiseGIFGenerator(width, height, frames, duration, pixel_size, output_path)
        thread = threading.Thread(target=self.run_task, args=(generator,))
        thread.start()

    def run_task(self, generator):
        """Запускает генерацию в потоке."""
        def progress_callback(current, total):
            self.progress['value'] = (current / total) * 100
            self.root.update_idletasks()

        output_path = generator.create_gif(progress_callback)
        if output_path:
            messagebox.showinfo("Готово!", f"GIF сохранен: {output_path}")
        else:
            messagebox.showerror("Ошибка", "Не удалось создать GIF.")

        self.create_button.config(state='normal')


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
