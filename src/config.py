import configparser
import os
import platform
from main import APP_NAME


def get_config_path(app_name=APP_NAME, file_name="config.ini") -> str:
    """
    Возвращает путь для хранения конфигурационного файла в зависимости от ОС.

    :param app_name: Имя приложения.
    :param file_name: Имя файла конфигурации.
    :return: Полный путь к файлу конфигурации.
    """
    system = platform.system()

    if system == "Darwin":  # macOS
        base_dir = os.path.join(os.path.expanduser("~"), "Library", "Application Support", app_name)
    elif system == "Windows":  # Windows
        base_dir = os.path.join(os.getenv("APPDATA"), app_name)
    else:  # Linux и другие Unix-подобные системы
        base_dir = os.path.join(os.path.expanduser("~"), f".{app_name.lower()}")

    os.makedirs(base_dir, exist_ok=True)  # Создаём директорию, если её нет
    return os.path.join(base_dir, file_name)


def load_config(app_name=APP_NAME, config_file=None):
    """
    Загружает параметры из конфигурационного файла.

    :param app_name: Имя приложения.
    :param config_file: Путь к конфигурационному файлу. Если не указан, используется стандартный путь.
    :return: Возвращает словарь с параметрами.
    """
    if config_file is None:
        config_file = get_config_path(app_name)

    settings = {}

    # Проверяем, существует ли конфигурационный файл
    if not os.path.exists(config_file):
        print(
            f"Предупреждение: файл конфигурации '{config_file}' не найден. Будет создан новый файл с параметрами по умолчанию."
        )
        create_default_config(app_name, config_file)
        return settings

    config = configparser.ConfigParser()
    config.read(config_file)

    settings['border_color'] = tuple(map(int, config.get('general', 'border_color', fallback="255,255,255").split(',')))

    # Чтение border_size с учётом возможных разных форматов
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
    settings['overwrite'] = config.getboolean('general', 'overwrite', fallback=False)
    settings['priority_mode'] = config.get('general', 'priority_mode', fallback='output_size')

    return settings


def create_default_config(app_name=APP_NAME, config_file=None):
    """
    Создаёт конфигурационный файл с параметрами по умолчанию.

    :param app_name: Имя приложения.
    :param config_file: Путь к конфигурационному файлу. Если не указан, используется стандартный путь.
    """
    if config_file is None:
        config_file = get_config_path(app_name)

    config = configparser.ConfigParser()

    # Добавляем секцию 'general' с дефолтными значениями
    config.add_section('general')
    config.set('general', 'overwrite', 'False')
    config.set('general', 'priority_mode', 'output_size')
    config.set('general', 'border_color', '255,255,255')
    config.set('general', 'border_size', '20')
    config.set('general', 'output_size', '1080,1080')
    config.set('general', 'min_border', '0')

    # Записываем файл
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    print(f"Создан новый файл конфигурации с параметрами по умолчанию: '{config_file}'")

