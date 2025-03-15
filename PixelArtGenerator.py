import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import imageio
import random
import os

# Функция для создания пиксельного изображения
def create_pixel_image(width, height, pixel_size):
    image = Image.new('RGB', (width * pixel_size, height * pixel_size), color='white')
    draw = ImageDraw.Draw(image)
    for y in range(height):
        for x in range(width):
            color = tuple(random.randint(0, 255) for _ in range(3))  # случайный цвет
            draw.rectangle([x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size], fill=color)
    return image

# Функция для создания анимированного gif
def create_animated_gif(width, height, pixel_size, duration, frames, quality):
    images = []
    for _ in range(frames):
        img = create_pixel_image(width, height, pixel_size)
        images.append(img)

    # Путь сохранения
    gif_path = save_path.get()
    if not gif_path:
        messagebox.showerror("Ошибка", "Путь для сохранения не выбран!")
        return

    # Сохранение GIF с учётом качества
    if quality == 'Высокое':
        imageio.mimsave(gif_path, images, duration=duration, quality=100)
    elif quality == 'Среднее':
        imageio.mimsave(gif_path, images, duration=duration, quality=50)
    else:  # Низкое качество
        imageio.mimsave(gif_path, images, duration=duration, quality=10)

    return gif_path

# Функция обработки кнопки "Создать"
def on_create():
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        pixel_size = int(pixel_size_entry.get())
        duration = float(duration_entry.get())
        frames = int(frames_entry.get())
        quality = quality_var.get()

        if width <= 0 or height <= 0 or pixel_size <= 0 or duration <= 0 or frames <= 0:
            raise ValueError("Все значения должны быть положительными.")

        gif_path = create_animated_gif(width, height, pixel_size, duration, frames, quality)
        if gif_path:
            messagebox.showinfo("Готово", f"GIF успешно создан и сохранён как {gif_path}")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Неверные данные: {str(e)}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

# Функция для выбора пути сохранения
def choose_save_path():
    file_path = filedialog.asksaveasfilename(defaultextension='.gif', filetypes=[("GIF Files", "*.gif")])
    if file_path:
        save_path.set(file_path)

# Создание графического интерфейса
root = tk.Tk()
root.title("Создание анимированного пиксельного GIF")
root.geometry("500x500")

# Переменная для хранения пути сохранения
save_path = tk.StringVar()

# Метки и поля ввода для параметров
tk.Label(root, text="Ширина (px):").pack()
width_entry = tk.Entry(root)
width_entry.pack()

tk.Label(root, text="Высота (px):").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Размер пикселя:").pack()
pixel_size_entry = tk.Entry(root)
pixel_size_entry.pack()

tk.Label(root, text="Длительность кадра (сек):").pack()
duration_entry = tk.Entry(root)
duration_entry.pack()

tk.Label(root, text="Количество кадров:").pack()
frames_entry = tk.Entry(root)
frames_entry.pack()

tk.Label(root, text="Выберите качество:").pack()
quality_var = tk.StringVar(value="Среднее")
tk.Radiobutton(root, text="Высокое", variable=quality_var, value="Высокое").pack()
tk.Radiobutton(root, text="Среднее", variable=quality_var, value="Среднее").pack()
tk.Radiobutton(root, text="Низкое", variable=quality_var, value="Низкое").pack()

# Кнопка для выбора пути сохранения
save_button = tk.Button(root, text="Выбрать место для сохранения", command=choose_save_path)
save_button.pack()

# Поле для отображения выбранного пути
save_path_label = tk.Label(root, textvariable=save_path)
save_path_label.pack()

# Кнопка для создания GIF
create_button = tk.Button(root, text="Создать GIF", command=on_create)
create_button.pack()

# Запуск интерфейса
root.mainloop()
