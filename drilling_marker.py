# import subprocess
# import sys
import msvcrt

# try:
#     from pynput.keyboard import Key, Controller
# except ImportError as e:
#     try:
#         print('Пробуем установить необходимую библиотеку.')
#         subprocess.check_call([sys.executable, "-m", "pip", "install", 'pynput'])
#     except:
#         print("""Скрипт не может установить пакет. Откройте командную строку, выполните следующее :
#                 pip install pynput """)

detail_measures = []
vertical_array = []
horizontal_array = []

detail_measures.append([float(item) for item in input('Введите размер детали X Y Z через пробел > ').split()])  # TODO: never used. We gonna use this in horizonal drilling.


print("""\rВЕРТИКАЛЬНОЕ СВЕРЛЕНИЕ.
Введите координаты через пробел. (x   y   l   T)
x, y  - координаты
l - глубина сверления
T - номер инструмента
Enter - добавить новое отверстие
Esc - закончить и сформировать инструкцию
 \r""")


vertical_array.append([float(item) for item in input('Введите переменные > ').split()])

with open('instruction.txt', 'w') as file:
    file.write("M6T1\rG43\rM3 S6000\r")

while True:

    print('Задать еще одно отверстие - Enter, закончить - Esc')
    key_press = msvcrt.getch()

    if ord(key_press) == 13:
        vertical_array.append([float(item) for item in input('Переменные > ').split()])
    elif ord(key_press) == 27:
        print(f'Создаем инструкцию.. \r{vertical_array}')

        with open('instruction.txt', 'a') as file:
            for coord_line in vertical_array:
                file.write(f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"
                           f"  Z18.0000\r"
                           f"G1 Z0.0000 F240\r"
                           f"G0 Z30.0000\r")

        break

# APPENDING HORIZONTAL DRILLING INSTRUCTIONS IF NEEDED

yes = ['yes', 'ye', 'y', 'д', 'да']

horizontal_prompt = input('Добавить горизонтальное сверление?  д/н  y/n')

if horizontal_prompt in yes:

    print("""\rГОРИЗОНТАЛЬНОЕ СВЕРЛЕНИЕ.
    Введите координаты через пробел. (x   y   l   T)
    x, y  - координаты
    l - глубина сверления
    T - номер инструмента
    Enter - добавить новое отверстие
    Esc - закончить и сформировать инструкцию
     \r""")

    horizontal_array.append([float(item) for item in input('Введите переменные > ').split()])

    while True:
        print('Задать еще одно отверстие - Enter, закончить - Esc')
        key_press = msvcrt.getch()

        if ord(key_press) == 13:
            vertical_array.append([float(item) for item in input('Переменные > ').split()])
        elif ord(key_press) == 27:
            print(f'Создаем инструкцию.. \r{vertical_array}')

print('\rГотово.')
