import subprocess
from subprocess import Popen
import sys
import os
import tkinter
from tkinter import ttk, filedialog

for lib in ['openpyxl', 'pandas']:

    try:
        import openpyxl
        import pandas as pd
    except ImportError as e:
        try:
            print(f'Установка {lib}...')
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
        except:
            print(f"Скрипт не может установить пакет. Откройте командную строку, выполните следующее :"
                  f"pip install {lib} ")

import pandas as pd

tool_json = {"1":{"номер инструмента": "1", "диаметр": "10", "тип" : "главсверло", "скорость вращения": "первая космическая", "подача": "30"},          #TODO: what do we do with this?
             "2":{"номер инструмента": "2", "диаметр": "12", "тип" : "еще сверло", "скорость вращения": "первая космическая", "подача": "22"}}


cwd = os.path.dirname(os.path.realpath(__file__))

window = tkinter.Tk()
window.geometry("640x320")
window.title('Drilling marker')

info_label = tkinter.Label(window, text='')
info_label.pack(pady=20)


def run_the_parameters():
    """this creates the dataframe using the parameters from the chosen file"""
    try:
        info_label.config(text='')
        filename = r"{}".format(parameters_chosen)
        global df
        df = pd.read_excel(filename, index_col=None, engine='openpyxl')

        global detail_measurments, vertical_array, horizontal_array

        detail_measurments = df[['X', 'Y', 'Z']].dropna().values.tolist()
        vertical_array = df[['X.1', 'Y.1', 'Глубина', '№ инструмента']].dropna().sort_values(by='№ инструмента').values.tolist()
        horizontal_array = df[['X.2', 'Y.2', 'Z.1', 'Глубина.1', '№ инструмента.1', 'Сторона']].dropna().sort_values(by='№ инструмента.1').values.tolist()

    except FileNotFoundError:
        print('Файл не найден, попробуйте выбрать и загрузить его заново.')


def choose_file():
    """this creates the parameter file variable after prompting"""
    global filename
    filename = filedialog.askopenfilename(
        initialdir=cwd,
        title="Открыть файл с параметрами",
        filetype=(("xlsx files", "*, xlsx"), ("All files", "*.*"))
    )
    if filename:
        global parameters_chosen
        parameters_chosen = filename
        open_param_button.config(state='normal')
        create_instruction_button.config(state='normal')
        param_file_chosen_entry.delete(0, 'end')
        param_file_chosen_entry.insert(0, filename)


def edit_file():
    """this opens the parameter file derived from chose_file() : global parameters_chosen """
    Popen(parameters_chosen, shell=True)


def fill_the_instruction():
    """this writes the instruction to the file specified"""
    save_file = filedialog.asksaveasfile(
        initialdir=cwd,
        mode='w',
        defaultextension=".txt",
        filetypes=[('Text Document', '*.txt'), ('All Files', '*.*')]
    )

    try:
        run_the_parameters()

        with open(f"{save_file.name}", 'w', encoding='utf8') as file:

            file.write(f"G21 G49 G80 G90 G91.1\r")
            for coord_line in vertical_array:
                file.write(f"\rM6T{int(coord_line[3])}\rG43\rM3 S6000\r"
                           f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"
                           f"  Z18.0000\r"
                           f"G1 Z0.0000 F240\r"
                           f"G0 Z30.0000\r")

            for coord_line in horizontal_array:
                file.write(f"\rM6T{int(coord_line[4])}\rG43\rM3 S6000\r"
                           f"\rG0 X{coord_line[0]:.4f} Y{coord_line[1]:.4f} Z30.0000\r"  # TODO ДОБАВИТЬ - + 100мм для размера головы инструмента
                           f"Z{coord_line[2]:.4f}\r")

                if coord_line[-1] == 1:
                    ex = 0 + coord_line[3]
                    file.write(f"Y{ex:.4f} F240\r"
                               f"Y0.0000\r")
                else:
                    ex = detail_measurments[0][1] - coord_line[3]
                    file.write(f"Y{ex:.4f} F240\r"
                               f"Y{detail_measurments[0][1]:.4f}\r")

            file.write(f"Z30.0000\r"
                       f"\rG0 Z50.0000\r"
                       f"G0 X0.0000 Y{detail_measurments[0][1]:.4f}\r"
                       f"M5\r"
                       f"M30\r")

            info_label.config(text='Готово')
    except:
        param_file_chosen_entry.delete(0, 'end')
        param_file_chosen_entry.insert(0, 'Ошибка чтения параметров, отредактируйте документ.')


choose_param_button = tkinter.Button(window, text="Выбрать файл с параметрами", command=choose_file)
choose_param_button.pack()

param_file_chosen_entry = tkinter.Entry(window, width=100)
param_file_chosen_entry.pack()

open_param_button = tkinter.Button(window, text="Редактировать параметры", state="disabled", command=edit_file)
open_param_button.pack()

create_instruction_button = tkinter.Button(window, text="Создать инструкцию c выбранными параметрами", state="disabled", command=fill_the_instruction)
create_instruction_button.pack()

exit_button = tkinter.Button(window, text="Выход", command=window.destroy)
exit_button.pack()


tkinter.mainloop()
