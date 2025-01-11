from PIL import Image, ImageOps

def add_border(
        image_path,
        output_path,
        border_color=(255, 255, 255),
        border_size=None,
        output_size=None,
        min_border=0
):
    """
    Добавляет рамку к изображению. Поддерживает два варианта:
    - Если задан output_size, то изображение масштабируется, чтобы поместиться в этот размер, и добавляется рамка.
    - Если задан border_size, то рамка фиксированного размера.

    :param image_path: Путь к исходному изображению.
    :param output_path: Путь для сохранения результата.
    :param border_color: Цвет рамки (RGB кортеж).
    :param border_size: Размер рамки (если фиксированная рамка), кортеж (left, top, right, bottom) или одно значение.
    :param output_size: Итоговый размер изображения (включая рамку), кортеж (width, height).
    :param min_border: Минимальная ширина рамки (если задан output_size).
    """
    # Открываем изображение
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Функция для округления до ближайшего чётного числа
    def make_even(value):
        return value if value % 2 == 0 else value + 1

    # Если задан output_size, рассчитываем рамки
    if output_size:
        output_width, output_height = output_size

        # Округляем размеры до ближайших чётных чисел
        output_width = make_even(output_width)
        output_height = make_even(output_height)

        # Вычисляем масштаб, чтобы вписать изображение в output_size с минимальной рамкой
        scale = min(
            (output_width - 2 * min_border) / img_width,
            (output_height - 2 * min_border) / img_height
        )

        new_width = int(img_width * scale)
        new_height = int(img_height * scale)

        # Масштабируем изображение
        img = img.resize((new_width, new_height), Image.LANCZOS)

        # Округляем размеры нового изображения до чётных чисел
        new_width = make_even(new_width)
        new_height = make_even(new_height)

        # Вычисляем размеры рамки
        left_border = (output_width - new_width) // 2
        top_border = (output_height - new_height) // 2
        right_border = output_width - new_width - left_border
        bottom_border = output_height - new_height - top_border
    elif border_size:
        # Если задан фиксированный размер рамки, обрабатываем три варианта:
        if isinstance(border_size, int):
            left_border = top_border = right_border = bottom_border = border_size
        elif isinstance(border_size, (tuple, list)):
            # Если 2 значения (по горизонтали и вертикали)
            if len(border_size) == 2:
                left_border = right_border = border_size[0]
                top_border = bottom_border = border_size[1]
            # Если 4 значения (по каждой стороне отдельно)
            elif len(border_size) == 4:
                left_border, top_border, right_border, bottom_border = border_size
            else:
                raise ValueError("border_size должен быть int, (left, top, right, bottom) или (horizontal, vertical)")
        else:
            raise ValueError("border_size должен быть int или (tuple, list)")

        # Округляем размеры рамки до чётных чисел
        left_border = make_even(left_border)
        top_border = make_even(top_border)
        right_border = make_even(right_border)
        bottom_border = make_even(bottom_border)
    else:
        raise ValueError("Необходимо задать либо border_size, либо output_size")

    # Добавляем рамку
    img_with_border = ImageOps.expand(
        img,
        border=(left_border, top_border, right_border, bottom_border),
        fill=border_color
    )

    # Сохраняем результат
    img_with_border.save(output_path, format="JPEG", quality=95, subsampling=0)