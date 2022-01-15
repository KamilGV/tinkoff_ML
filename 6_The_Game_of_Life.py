import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

TICK = 150
SIZE = 500
GRID_VALUES = ["10", "50", "100"]
RANDOM_GENERATOR_VALUE = 0.75
COLORS = ['red', 'gray']
INFO = '''Инструкция:\n
            1.Выберите размер сетки в выпадающем списке слева.
            2.Заполните поле вручную,нажимая левой кнопкой мыши по ячейкам,
            либо сгенирируйте случайное поле, нажав на кнопку 'Random'.
            3.Нажмите кнопку 'Start' для запуска игры.
            4.Наблюдейте за игрой.
            5.Игру можно остановить нажав на кнопку 'Stop'.'''


class Cell:
    def __init__(self):
        self.active = False

    def get_active(self):
        return self.active

    def set_active_true(self):
        self.active = True

    def set_active_false(self):
        self.active = False


class Field:
    def __init__(self, size):
        self.size = size
        self.grid = [[Cell() for c in range(size)] for r in range(size)]

    def get_size(self):
        return self.size

    def set_active_cell_false(self, row, column):
        self.grid[row][column].set_active_false()

    def set_active_cell_true(self, row, column):
        self.grid[row][column].set_active_true()

    def get_cell_value(self, row, column):
        return self.grid[row][column].get_active()

    def get_number_neighbours_active(self, row, column):
        number = 0
        if row == 0 and column == 0:
            if self.get_cell_value(1, 0):
                number += 1
            if self.get_cell_value(0, 1):
                number += 1
            if self.get_cell_value(1, 1):
                number += 1
            return number
        elif row == self.size-1 and column == self.size-1:
            if self.get_cell_value(self.size-1, self.size-2):
                number += 1
            if self.get_cell_value(self.size-2, self.size-1):
                number += 1
            if self.get_cell_value(self.size-2, self.size-2):
                number += 1
            return number
        elif row == 0 and column == self.size-1:
            if self.get_cell_value(0, self.size-2):
                number += 1
            if self.get_cell_value(1, self.size-1):
                number += 1
            if self.get_cell_value(1, self.size-2):
                number += 1
            return number
        elif row == self.size-1 and column == 0:
            if self.get_cell_value(self.size-2, 0):
                number += 1
            if self.get_cell_value(self.size-1, 1):
                number += 1
            if self.get_cell_value(self.size-2, 1):
                number += 1
            return number
        elif row == 0:
            if self.get_cell_value(0, column-1):
                number += 1
            if self.get_cell_value(0, column+1):
                number += 1
            if self.get_cell_value(1, column):
                number += 1
            if self.get_cell_value(1, column+1):
                number += 1
            if self.get_cell_value(1, column-1):
                number += 1
            return number
        elif row == self.size-1:
            if self.get_cell_value(self.size-1, column-1):
                number += 1
            if self.get_cell_value(self.size-1, column+1):
                number += 1
            if self.get_cell_value(self.size-2, column):
                number += 1
            if self.get_cell_value(self.size-2, column+1):
                number += 1
            if self.get_cell_value(self.size-2, column-1):
                number += 1
            return number
        elif column == 0:
            if self.get_cell_value(row-1, 0):
                number += 1
            if self.get_cell_value(row+1, 0):
                number += 1
            if self.get_cell_value(row, 1):
                number += 1
            if self.get_cell_value(row+1, 1):
                number += 1
            if self.get_cell_value(row-1, 1):
                number += 1
            return number
        elif column == self.size-1:
            if self.get_cell_value(row-1, self.size-1):
                number += 1
            if self.get_cell_value(row+1, self.size-1):
                number += 1
            if self.get_cell_value(row, self.size-2):
                number += 1
            if self.get_cell_value(row+1, self.size-2):
                number += 1
            if self.get_cell_value(row-1, self.size-2):
                number += 1
            return number
        else:
            if self.get_cell_value(row-1, column-1):
                number += 1
            if self.get_cell_value(row+1, column+1):
                number += 1
            if self.get_cell_value(row-1, column+1):
                number += 1
            if self.get_cell_value(row+1, column-1):
                number += 1
            if self.get_cell_value(row, column-1):
                number += 1
            if self.get_cell_value(row, column+1):
                number += 1
            if self.get_cell_value(row-1, column):
                number += 1
            if self.get_cell_value(row+1, column):
                number += 1
            return number


class App(tk.Tk):
    def __init__(self, handler):
        super().__init__()
        self.title('Игра "Жизнь"')
        self.canv = tk.Canvas(self, width=SIZE, height=SIZE, bg='white')
        self.resizable(False, False)
        self.handler = handler
        self.label = tk.Label(self, text='Size: ')
        self.combo = ttk.Combobox(
            self,
            width=15,
            values=GRID_VALUES)
        self.button_start = tk.Button(
            self,
            text='Start',
            width=15,
            command=self.handler.start_process)
        self.button_stop = tk.Button(
            self,
            text='Stop',
            width=15,
            command=self.handler.stop_process)
        self.button_random_generation = tk.Button(
            self,
            text='Random',
            width=15,
            command=self.handler.random_generate_field)
        self.button_clear = tk.Button(
            self,
            text='Clear',
            width=15,
            command=self.handler.clear_field)
        self.button_info = tk.Button(
            self,
            text='User guide',
            width=15,
            command=self.onInfo)
        self.label.grid(row=0, column=0, columnspan=1)
        self.combo.grid(row=0, column=1, columnspan=1)
        self.button_start.grid(row=0, column=2, columnspan=1)
        self.button_stop.grid(row=0, column=3, columnspan=1)
        self.button_clear.grid(row=0, column=4, columnspan=1)
        self.button_random_generation.grid(row=0, column=5, columnspan=1)
        self.button_info.grid(row=0, column=6, columnspan=1)
        self.canv.grid(row=1, column=0, columnspan=10)
        self.canv.bind('<Button-1>', self.handler.set_cell_active)
        self.combo.bind("<<ComboboxSelected>>", self.handler.set_field)
        self.combo.set("Выберите размеры")
        self.button_start['state'] = 'disabled'
        self.button_random_generation['state'] = 'disabled'
        self.button_stop['state'] = 'disabled'
        self.button_clear['state'] = 'disabled'

    def onInfo(self):
        messagebox.showinfo("User's Manual", INFO)

    def lock_buttons(self):
        self.button_start['state'] = 'disabled'
        self.button_random_generation['state'] = 'disabled'
        self.combo['state'] = 'disabled'
        self.button_clear['state'] = 'disabled'

    def unlock_buttons(self):
        self.button_start['state'] = 'normal'
        self.button_random_generation['state'] = 'normal'
        self.button_stop['state'] = 'normal'
        self.combo['state'] = 'normal'
        self.button_clear['state'] = 'normal'

    def draw_line(self, x1, y1, x2, y2):
        self.canv.create_line(x1, y1, x2, y2, fill=COLORS[1])

    def draw_square(self, x1, y1, x2, y2):
        self.canv.create_rectangle(x1, y1, x2, y2, fill=COLORS[0])

    def get_combo_value(self):
        return self.combo.get()


class Handler:
    def __init__(self):
        self.view = None
        self.field = None
        self.process_activ = False

    def set_field(self, event):
        self.stop_process()
        size = int(self.view.get_combo_value())
        self.field = Field(size)
        self.view.unlock_buttons()
        self.draw_field()

    def clear_field(self):
        size = self.field.get_size()
        self.field = Field(size)
        self.draw_field()

    def random_generate_field(self):
        if self.field is None:
            return
        size = int(self.view.combo.get())
        self.field = Field(size)
        for i in range(self.field.get_size()):
            for y in range(self.field.get_size()):
                if random.random() > RANDOM_GENERATOR_VALUE:
                    self.field.set_active_cell_true(i, y)
        self.draw_field()

    def start_process(self):
        if self.process_activ:
            return
        self.process_activ = True
        self.view.lock_buttons()
        self.start_cicle()

    def start_cicle(self):
        size = self.field.get_size()
        buffer_field = Field(size)
        for i in range(size):
            for y in range(size):
                number = self.field.get_number_neighbours_active(i, y)
                if ((number == 2 or number == 3) and
                        self.field.get_cell_value(i, y)):
                    buffer_field.set_active_cell_true(i, y)
                elif (number == 3) and not self.field.get_cell_value(i, y):
                    buffer_field.set_active_cell_true(i, y)
                else:
                    buffer_field.set_active_cell_false(i, y)

        self.field = buffer_field
        self.draw_field()
        self.cicle = self.view.after(TICK, self.start_cicle)

    def stop_process(self):
        if self.process_activ:
            self.view.after_cancel(self.cicle)
            self.process_activ = False
            self.view.unlock_buttons()

    def set_cell_active(self, event):
        if self.field is not None and self.process_activ is False:
            size = self.field.get_size()
            step = SIZE/size
            x = int(event.x//step)
            y = int(event.y//step)
            if self.field.get_cell_value(x, y):
                self.field.set_active_cell_false(x, y)
            else:
                self.field.set_active_cell_true(x, y)
            self.draw_field()

    def draw_field(self):
        self.view.canv.delete("all")
        size = self.field.get_size()
        step = SIZE/size
        for i in range(size):
            for y in range(size):
                if self.field.get_cell_value(i, y):
                    self.view.draw_square(step*i, step*y,
                                          (1+i)*step, (1+y)*step)
        for i in range(int(SIZE/step)):
            self.view.draw_line(0, i*step, SIZE, i*step)
        for i in range(int(SIZE/step)):
            self.view.draw_line(i*step, 0, i*step, SIZE)

    def set_view(self, view):
        self.view = view

if __name__ == '__main__':
    handler = Handler()
    view = App(handler)
    handler.set_view(view)
    view.mainloop()
