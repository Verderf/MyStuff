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

detail_measurments = []
vertical_array = []
horizontal_array = []

detail_measurments.append([float(item) for item in input('Введите размер детали X Y Z через пробел > ').split()])

print(detail_measurments)

print("""\rВЕРТИКАЛЬНОЕ СВЕРЛЕНИЕ.
Введите координаты точки через пробел. (x   y   l   T)
x, y  - координаты
l - глубина сверления
T - номер инструмента
Enter - добавить новое отверстие
Esc - закончить и сформировать инструкцию
 \r""")


vertical_array.append([float(item) for item in input('Введите переменные > ').split()])

with open('instruction.txt', 'w') as file:
    file.write("\r")

while True:

    print('Задать еще одно отверстие - Enter, закончить - Esc')
    key_press = msvcrt.getch()

    if ord(key_press) == 13:
        vertical_array.append([float(item) for item in input('Переменные > ').split()])

    elif ord(key_press) == 27:

        for array_item in vertical_array:
            if len(array_item) != 4:                # TODO : out-of-boundary exceptions
                print(f'Некорректно введеные координаты будут игнорироваться: {array_item}')
                vertical_array.remove(array_item)

        print('Координаты вертикального сверления :')
        for i in vertical_array:
            print(f'{i}\r')

        with open('instruction.txt', 'a') as file:
            for coord_line in vertical_array:
                file.write(f"\rM6T{int(coord_line[3])}\rG43\rM3 S6000\r"
                           f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"
                           f"  Z18.0000\r"
                           f"G1 Z0.0000 F240\r"
                           f"G0 Z30.0000\r")

        break

# APPENDING HORIZONTAL DRILLING INSTRUCTIONS IF NEEDED

yes = ['да', 'д']

horizontal_prompt = input('Добавить горизонтальное сверление? д/н ')

if horizontal_prompt in yes:

    print("""\rГОРИЗОНТАЛЬНОЕ СВЕРЛЕНИЕ.
    Введите координаты точки через пробел. (x   y   z   l   T   S)
    x, y, z  - координаты
    l - глубина сверления
    T - номер инструмента
    S - сторона
    Enter - добавить новое отверстие
    Esc - закончить и сформировать инструкцию
     \r""")

    horizontal_array.append([float(item) for item in input('Введите переменные > ').split()])

    while True:

        print('Задать еще одно отверстие - Enter, закончить - Esc')
        key_press = msvcrt.getch()

        if ord(key_press) == 13:
            horizontal_array.append([float(item) for item in input('Переменные > ').split()])
        elif ord(key_press) == 27:

            for array_item in horizontal_array:
                if len(array_item) != 6:
                    print(f'Некорректно введеные координаты будут игнорироваться: {array_item}')
                    horizontal_array.remove(array_item)

            print('Координаты горизонтального сверления :')
            for i in horizontal_array:
                print(f'{i}\r')

            with open('instruction.txt', 'a') as file:
                for coord_line in horizontal_array:
                    file.write(f"\rM6T{int(coord_line[4])}\rG43\rM3 S6000\r"
                               f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"
                               f"Z{coord_line[2]:.4f}\r")

                    if coord_line[-1] == 1:
                        ex = 0 + coord_line[3]
                        file.write(f"Y{ex:.4f} F240\r"
                                   f"Y0.0000\r")
                    else:                                                       # TODO: do the exceptions on third side
                        ex = detail_measurments[0][1] - coord_line[3]
                        file.write(f"Y{ex:.4f} F240\r"
                                   f"Y{detail_measurments[0][1]:.4f}\r")

                    file.write(f"Z30.0000\r")

            break

print('\rГотово.')
