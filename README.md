# EasyFrame
A small utility for adding frames to pictures in jpg format

Параметры запуска
 ```
--output Путь для сохранения результата
--config Путь к конфигурационному файлу
--border_size Размер рамки
--output_size Итоговый размер изображения (в формате width,height)
--min_border Минимальный размер рамки для режима итогового размера
--border_color Цвет рамки (в формате R,G,B)
```
Команда для компиляции
```
pyinstaller --name EasyFrame --distpath ../dist/mac --windowed --icon=../icons/icon-mac.icns main.py
```