import argparse
import config
import os
from add_border import add_border


def main():
    parser = argparse.ArgumentParser(description="Добавить рамку к изображению.")

    # Опциональные параметры
    parser.add_argument("input", nargs="?", help="Путь к исходному изображению.")
    parser.add_argument("--output", nargs="?", help="Путь для сохранения результата.")
    parser.add_argument("--config", default="config.ini", help="Путь к конфигурационному файлу.")
    parser.add_argument("--border_size", type=str, help="Размер рамки.")
    parser.add_argument("--output_size", type=str, help="Итоговый размер изображения (в формате width,height).")
    parser.add_argument("--min_border", type=int, help="Минимальный размер рамки для режима итогового размера")
    parser.add_argument("--border_color", type=str, help="Цвет рамки (в формате R,G,B).")

    # Перехват аргументов и обработка ошибок
    args = parser.parse_args()

    # Загружаем настройки из конфигурационного файла
    config_settings = config.load_config(args.config)
    overwrite = bool(config_settings.get('overwrite'))

    # Проверяем корректность аргументов
    if not args.input:
        print("Ошибка: необходимо указать входной файл.")
        parser.print_help()
        return
    elif not os.path.exists(args.input):
        print("Ошибка: указанный файл не существует.")
        parser.print_help()
        return

    if not overwrite and not args.output:
        print("Ошибка: необходимо указать выходной файл, если перезапись отключена.")
        parser.print_help()
        return

    # Устанавливаем файлы ввода и вывода
    input_file = args.input
    output_file = args.input if overwrite else args.output


    # Применяем параметры из командной строки, если они заданы
    if args.border_color:
        border_color = tuple(map(int, args.border_color.split(',')))
    else:
        border_color = config_settings.get('border_color', (255, 255, 255))

    border_size = None
    output_size = None
    min_border = 0

    if args.border_size:
        try:
            border_size = eval(args.border_size)  # Преобразуем строку в кортеж или число
        except Exception:
            border_size = 20

    if args.output_size:
        output_size = tuple(map(int, args.output_size.split(',')))
        if args.min_border:
            min_border = args.min_border
        else:
            min_border = config_settings.get('min_border', 0)

    # Логика для проверки
    if border_size and output_size:
        if config_settings.get('priority_mode') == 'output_size':
            border_size = None
        elif config_settings.get('priority_mode') == 'border_size':
            output_size = None
        else:
            print("Ошибка: в конфигурации не указвн приоритет, при этом заданы взаимоисключающие параметры.")
            parser.print_help()
            return

    # Если ни один из параметров не задан, берем из конфига
    if not border_size and not output_size:
        if config_settings.get('priority_mode') == 'output_size':
            border_size = None
            output_size = config_settings.get('output_size', '1080,1080')
        elif config_settings.get('priority_mode') == 'border_size':
            border_size = config_settings.get('border_size', 20)
            output_size = None
        else:
            print("Ошибка: неверный параметр priority_mode в конфигурации.")
            print(config_settings.get('priority_mode'))
            parser.print_help()
            return


    # Вызываем функцию добавления рамки
    add_border(
        input_file,
        output_file,
        border_color=border_color,
        border_size=border_size,
        output_size=output_size,
        min_border=min_border
    )


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass