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

detail_measures.append([float(item) for item in input('Введите размер детали X Y Z через пробел > ').split()])

print(detail_measures)

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
    file.write(f"G21 G49 G80 G90 G91.1\r")

while True:

    print('Задать еще одно отверстие - Enter, закончить - Esc')
    key_press = msvcrt.getch()

    if ord(key_press) == 13:
        vertical_array.append([float(item) for item in input('Переменные > ').split()])
    elif ord(key_press) == 27:
        print(f'Создаем инструкцию.. \r{vertical_array}')

        with open('instruction.txt', 'a') as file:
            for coord_line in vertical_array:
                file.write(f"\rM6T{int(coord_line[3])}\rG43\rM3 S6000\r"
                           f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"
                           f"  Z18.0000\r"
                           f"G1 Z0.0000 F240\r"
                           f"G0 Z30.0000\r")

        break

# APPENDING HORIZONTAL DRILLING INSTRUCTIONS IF NEEDED

yes = ['yes', 'ye', 'y', 'д', 'да']

horizontal_prompt = input('Добавить горизонтальное сверление?  д/н  y/n ')

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
            print(f'Создаем инструкцию.. \r{vertical_array}')

            with open('instruction.txt', 'a') as file:
                for coord_line in horizontal_array:
                    file.write(f"\rM6T{int(coord_line[4])}\rG43\rM3 S6000\r"
                               f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"
                               f"Z{coord_line[2]:.4f}\r")

                    if coord_line[-1] == 1:
                        ex = 0 + coord_line[3]
                        file.write(f"Y{ex:.4f} F240\r"
                                   f"Y0.0000\r")
                    else:                                                                   # TODO: do the exceptions on third side
                        ex = detail_measures[0][1] - coord_line[3]
                        file.write(f"Y{ex:.4f} F240\r"
                                   f"Y{detail_measures[0][1]:.4f}\r")

                    file.write(f"Z30.0000\r"
                               f"G0Z50.0000\r"
                               f"G0X0.0000Y{detail_measures[0][1]:.4f}\r"
                               f"M5\r"
                               f"M30\r")

            break

print('\rГотово.')

# TODO
"""
1) json collection for the tool
   номер  диаметр   тип   скорость вращ      подача

недоступно для оператора

2) отдельный инпут для каждого значения размеров детали с возможностью корректировки

3) вертикальное отверстие - то же самое

4) перевести инпут для отверстий в эксель

5) привязать интерфейс ко всему этому чтобы висели координаты видимые

6) сделать так, чтобы спрашивал, куда сохранять и с каким именем

мелочевка : 

сгруппировать по номеру инструмента, чтобы не менялись на ходу. 

exception handling for detail dimensions


"""