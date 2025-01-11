import configparser
import os


def load_config(config_file="config.ini"):
    """
    Загружает параметры из конфигурационного файла.

    :param config_file: Путь к конфигурационному файлу.
    :return: Возвращает словарь с параметрами.
    """
    settings = {}

    # Проверяем, существует ли конфигурационный файл
    if not os.path.exists(config_file):
        print(
            f"Предупреждение: файл конфигурации '{config_file}' не найден. Будет создан новый файл с параметрами по умолчанию.")
        create_default_config(config_file)
        return settings

    config = configparser.ConfigParser()
    config.read(config_file)

    settings['border_color'] = tuple(map(int, config.get('general', 'border_color', fallback="255,255,255").split(',')))

    # Чтение border_size с учетом возможных разных форматов
    border_size = config.get('general', 'border_size', fallback="20")
    try:
        border_size = eval(border_size)
    except Exception:
        border_size = 20

    settings['border_size'] = border_size

    # Чтение output_size, если задан
    output_size = config.get('general', 'output_size', fallback=None)
    if output_size:
        settings['output_size'] = tuple(map(int, output_size.split(',')))
    else:
        settings['output_size'] = None

    settings['min_border'] = config.getint('general', 'min_border', fallback=8)
    settings['overwrite'] = config.getboolean('general', 'ovwerwrite', fallback=False)
    settings['priority_mode'] = config.get('general', 'priority_mode', fallback='output_size')

    return settings


def create_default_config(config_file="config.ini"):
    """
    Создаёт конфигурационный файл с параметрами по умолчанию.
    """
    config = configparser.ConfigParser()

    # Добавляем секцию 'general' с дефолтными значениями
    config.add_section('general')
    config.set('general', 'overwrite', 'False')
    config.set('general', 'priority_mode', 'output_size')
    config.set('general', 'border_color', '255,255,255')
    config.set('general', 'border_size', '20')
    config.set('general', 'output_size', '1080,1080')
    config.set('general', 'min_border', '8')

    # Записываем файл
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    print(f"Создан новый файл конфигурации с параметрами по умолчанию: '{config_file}'")

