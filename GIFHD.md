# @ GIFHD

# Этот скрипт является отличным инструментом для создания пиксельных анимаций в формате GIF. Он подходит как для начинающих, так и для опытных пользователей, которым нужно быстро создать анимацию для веб-страниц, графических проектов или социальных сетей. В сочетании с возможностью настройки качества и параметров изображения, приложение предлагает максимальную гибкость для любых нужд.

# Импорт библиотек:
`import tkinter as tk`
`from tkinter import filedialog, messagebox`
`from PIL import Image, ImageDraw`
`import imageio`
`import random`
`import os`

![01](https://github.com/user-attachments/assets/a506ca2b-72b4-4fc1-a4c1-818ee72fdb04)

# Для работы программы используется несколько ключевых библиотек:
Tkinter — для создания графического интерфейса.
PIL (Python Imaging Library) — для работы с изображениями, в частности для рисования пикселей.
Imageio — для создания и сохранения анимации в формате GIF.
Random — для генерации случайных цветов пикселей.

Функция создания пиксельного изображения:
`def create_pixel_image(width, height, pixel_size):
    image = Image.new('RGB', (width * pixel_size, height * pixel_size), color='white')
    draw = ImageDraw.Draw(image)
    for y in range(height):
        for x in range(width):
            color = tuple(random.randint(0, 255) for _ in range(3))  # случайный цвет
            draw.rectangle([x * pixel_size, y * pixel_size, (x + 1) * pixel_size, (y + 1) * pixel_size], fill=color)
    return image`
# Эта функция создаёт изображение с заданными параметрами:
width и height — ширина и высота в пикселях.
pixel_size — размер каждого пикселя (который на самом деле является прямоугольником на изображении).
Каждый пиксель рисуется случайным цветом, что создает разнообразие и уникальность для каждого кадра.

# Функция для создания анимации (GIF)
`def create_animated_gif(width, height, pixel_size, duration, frames, quality):
    images = []
    for _ in range(frames):
        img = create_pixel_image(width, height, pixel_size)
        images.append(img)`

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

    return gif_path` 

# Эта функция генерирует анимированный GIF:
Создаются несколько кадров (указано количество через frames).
Каждый кадр — это новое случайное пиксельное изображение.
GIF сохраняется с учетом указанного качества и длительности кадров.

# Качество анимации можно настроить с тремя уровнями:
Высокое — для четких, качественных изображений.
Среднее — баланс между качеством и размером файла.
Низкое — для уменьшения размера файла (идеально для веб-использования).

# Функция обработки кнопки "Создать"
`def on_create():
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        pixel_size = int(pixel_size_entry.get())
        duration = float(duration_entry.get())
        frames = int(frames_entry.get())
        quality = quality_var.get()`

        if width <= 0 or height <= 0 or pixel_size <= 0 or duration <= 0 or frames <= 0:
            raise ValueError("Все значения должны быть положительными.")

        gif_path = create_animated_gif(width, height, pixel_size, duration, frames, quality)
        if gif_path:
            messagebox.showinfo("Готово", f"GIF успешно создан и сохранён как {gif_path}")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Неверные данные: {str(e)}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")`

# Эта функция управляет процессом создания GIF. 
Она:
Считывает данные с графического интерфейса (ширина, высота, размер пикселей и т.д.).
Проверяет, что все значения положительные.
Генерирует GIF с помощью функции create_animated_gif.
Если всё прошло успешно, выводится сообщение с информацией о том, где был сохранён файл.

# Выбор пути сохранения:
`def choose_save_path():
    file_path = filedialog.asksaveasfilename(defaultextension='.gif', filetypes=[("GIF Files", "*.gif")])
    if file_path:
        save_path.set(file_path)`
Эта функция позволяет пользователю выбрать, куда сохранить созданный GIF-файл. Открывается стандартный диалог сохранения, и путь сохраняется в переменной save_path.

# Преимущества скрипта
Простота использования: благодаря графическому интерфейсу пользователи легко могут настроить параметры GIF, даже если не имеют опыта работы с кодом.
# Гибкость: можно изменять размеры, количество кадров, длительность и качество, что дает пользователю возможность адаптировать GIF под свои нужды.
# Производительность: генерация случайных цветов пикселей делает каждое изображение уникальным, а анимация выглядит динамично и красочно.
