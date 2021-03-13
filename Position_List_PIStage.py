import tkinter as tk
from tkinter import filedialog
import time

import numpy as np

from pipython import GCSDevice, pitools


class PositionList(tk.Frame):

    def __init__(self, root, c867, e518):

        self.e518 = e518
        self.x = self.e518.axes[1]
        self.y = self.e518.axes[0]
        self.z = self.e518.axes[2]
        self.c867 = c867
        self.mox = self.c867.axes[0]
        self.moy = self.c867.axes[1]

        self.popup_win = tk.Toplevel(root)
        self.popup_win.wm_title("Position list")
        self.popup_win.geometry('700x800')
        self.popup_win.configure(bg='white')
        self.popup_win.resizable(0, 0)

        self.absolute_btn = tk.Button(self.popup_win,
                                      text='Absolute Position',
                                      font='Arial 12',
                                      width=31,
                                      command=self.set_absolute_pos)
        self.absolute_btn.place(relx=0.05, rely=0.02)
        self.relative_btn = tk.Button(self.popup_win,
                                      text='Relative Position',
                                      font='Arial 12',
                                      width=31,
                                      command=self.set_relative_pos)
        self.relative_btn.place(relx=0.52, rely=0.02)
        interval = 0.068
        self.add_btn = tk.Button(self.popup_win,
                                 text='Add',
                                 font='Arial 12',
                                 width=12,
                                 command=self.add_position)
        self.add_btn.place(relx=0.79, rely=0.112)

        self.remove_btn = tk.Button(self.popup_win,
                                    text='Remove',
                                    font='Arial 12',
                                    width=12,
                                    command=self.remove_position)
        self.remove_btn.place(relx=0.79, rely=0.112+interval)

        self.clean_btn = tk.Button(self.popup_win,
                                   text='Clean',
                                   font='Arial 12',
                                   width=12,
                                   command=self.clean_position)
        self.clean_btn.place(relx=0.79, rely=0.112+(interval*2))

        self.insert_btn = tk.Button(self.popup_win,
                                    text='Insert',
                                    font='Arial 12',
                                    width=12,
                                    command=self.insert_position)
        self.insert_btn.place(relx=0.79, rely=0.112+(interval*3))

        self.replace_btn = tk.Button(self.popup_win,
                                     text='Replace',
                                     font='Arial 12',
                                     width=12,
                                     command=self.replace_position)
        self.replace_btn.place(relx=0.79, rely=0.112+(interval*4))

        self.update_btn = tk.Button(self.popup_win,
                                    text='Update',
                                    font='Arial 12',
                                    width=12,
                                    command=self.update_position)
        self.update_btn.place(relx=0.79, rely=0.112+(interval*5))

        self.go_btn = tk.Button(self.popup_win,
                                text='Go',
                                font='Arial 12',
                                width=12,
                                command=self.go)
        self.go_btn.place(relx=0.79, rely=0.112+(interval*6))

        self.start_btn = tk.Button(self.popup_win,
                                   text='Start',
                                   font='Arial 12',
                                   width=12,
                                   command=self.start)
        self.start_btn.place(relx=0.79, rely=0.112+(interval*7))

        self.save_btn = tk.Button(self.popup_win,
                                  text='Save',
                                  font='Arial 12',
                                  width=12,
                                  command=self.save)
        self.save_btn.place(relx=0.79, rely=0.112+(interval*8)+0.023)

        self.load_btn = tk.Button(self.popup_win,
                                  text='Load',
                                  font='Arial 12',
                                  width=12,
                                  command=self.load)
        self.load_btn.place(relx=0.79, rely=0.112+(interval*9)+0.023)

        self.close_btn = tk.Button(self.popup_win,
                                   text='Close',
                                   font='Arial 12',
                                   width=12,
                                   command=root.destroy)
        self.close_btn.place(relx=0.79, rely=0.112+(interval*10)+0.045)

        self.period_label = tk.Label(self.popup_win,
                                     text='Interval (min):',
                                     font='Arial 12', bg='white')
        self.period_label.place(relx=0.02, rely=0.91)
        self.period = tk.Entry(self.popup_win, font='Arial 12', width=5)
        self.period.place(relx=0.17, rely=0.91)

        self.nb_loop_label = tk.Label(self.popup_win,
                                      text='Number of loops:',
                                      font='Arial 12', bg='white')
        self.nb_loop_label.place(relx=0.27, rely=0.91)
        self.nb_loop = tk.Entry(self.popup_win, font='Arial 12', width=5)
        self.nb_loop.place(relx=0.46, rely=0.91)
        self.nb = 1

        self.filepath_label = tk.Label(self.popup_win, text='File path:',
                                       font='Arial 12', bg='white')
        self.filepath_label.place(relx=0.02, rely=0.96)
        self.filepath = tk.Entry(self.popup_win, font='Arial 12', width=49)
        self.filepath.place(relx=0.13, rely=0.96)

        self.ref_pos_label = tk.Label(self.popup_win, text='Ref. pos:',
                                      font='Arial 12', bg='white')
        self.ref_pos_label.place(relx=0.015, rely=0.07)
        self.pre_ref = ''
        self.cur_ref = ''
        self.ref_pos_list = []
        self.ref_position = tk.StringVar()
        self.ref_pos = tk.Entry(self.popup_win, font='Arial 12', width=38, textvariable=self.ref_position)
        self.ref_pos.place(relx=0.12, rely=0.074)
        self.set_ref = tk.Button(self.popup_win,
                                 text='Set ref.',
                                 font='Arial 12',
                                 width=8,
                                 command=self.set_ref_position)
        self.set_ref.place(relx=0.64, rely=0.07)
        self.ref_pos_label.place_forget()
        self.ref_pos.place_forget()
        self.set_ref.place_forget()

        self.position_list = []
        self.pos_list = tk.StringVar()
        self.position_listbox = tk.Listbox(self.popup_win,
                                           bg='white',
                                           font='Arial 12',
                                           height=20,
                                           listvariable=self.pos_list,
                                           selectmode=tk.SINGLE)
        self.position_listbox.place(relx=0.01, rely=0.11, relwidth=0.75, relheight=0.77)


    def set_absolute_pos(self):
        self.absolute_btn['relief'] = tk.SUNKEN
        self.relative_btn['relief'] = tk.RAISED
        self.ref_pos_label.place_forget()
        self.ref_pos.place_forget()
        self.set_ref.place_forget()

    def set_relative_pos(self):
        self.absolute_btn['relief'] = tk.RAISED
        self.relative_btn['relief'] = tk.SUNKEN
        self.ref_pos_label.place(relx=0.015, rely=0.07)
        self.ref_pos.place(relx=0.12, rely=0.074)
        self.set_ref.place(relx=0.64, rely=0.07)

    def set_ref_position(self):
        cur_pos = self.get_current_position()
        ref_pos = cur_pos['motor'] + cur_pos['piezo']
        self.ref_position.set(str(ref_pos))
        self.cur_ref = self.ref_position.get()

    def add_position(self):
        index = int(self.position_listbox.size())
        pos = self.get_formatted_position(index)
        self.position_list.append(pos)
        self.pos_list.set(self.position_list)

    def remove_position(self):
        item = self.position_listbox.curselection()
        if len(item) != 0:
            index = item[0]
            self.position_listbox.delete(item)
            self.position_list.pop(index)
            self.update_position_list(self.position_list)

    def clean_position(self):
        self.pos_list.set('')
        self.position_list = []

    def insert_position(self):
        item = self.position_listbox.curselection()
        if len(item) != 0:
            index = item[0]
            pos = self.get_formatted_position(index)
            self.position_listbox.insert(index, pos)
            self.position_list.insert(index, pos)
            self.update_position_list(self.position_list)

    def replace_position(self):
        item = self.position_listbox.curselection()
        if len(item) != 0:
            index = item[0]
            pos = self.get_formatted_position(index)
            self.position_list[index] = pos
            self.pos_list.set(self.position_list)

    def update_position(self):
        if self.relative_btn['relief'] == 'sunken':
            if self.pre_ref == '':
                self.pre_ref = self.cur_ref
            self.ref_pos_list = self.position_list
            if self.cur_ref != '' and len(self.ref_pos_list) != 0:
                pre_pos = eval(self.pre_ref)
                cur_pos = eval(self.cur_ref)
                diff_pos = [pre-cur for pre, cur in zip(pre_pos, cur_pos)]
                update_position_list = []
                for i, pos in enumerate(self.ref_pos_list):
                    pos_dic = self.get_valid_position(pos)
                    pos_list = pos_dic['motor'] + pos_dic['piezo']
                    new_list = [float((pre-diff).__format__('.4f')) for pre, diff in zip(pos_list, diff_pos)]
                    new_pos = self.get_formatted_position(index=i, motor=new_list[:2], piezo=new_list[2:])
                    update_position_list.append(new_pos)
                self.position_list = update_position_list
                self.pos_list.set(self.position_list)

    def go(self):
        item = self.position_listbox.curselection()
        if len(item) != 0:
            self.go_btn['state'] = tk.DISABLED
            index = item[0]
            pos = self.position_list[index]
            position_dic = self.get_valid_position(pos)
            self.move(position_dic['motor'], position_dic['piezo'])
            self.go_btn['state'] = tk.NORMAL

    def start(self):
        self.position_listbox.selection_clear(0, tk.END)
        self.start_btn['state'] = tk.DISABLED
        for i, pos in enumerate(self.position_list):
            self.position_listbox.selection_set(i)
            if i == 0:
                list_length = len(self.position_list)
                if list_length != 1:
                    self.position_listbox.selection_clear(list_length-1)
            else:
                self.position_listbox.selection_clear(i-1)
            self.position_listbox.update()
            pos = self.position_list[i]
            position_dic = self.get_valid_position(pos)
            self.move(position_dic['motor'], position_dic['piezo'])
            self.c867.SVO(self.mox, False)
            self.c867.SVO(self.moy, False)
            time.sleep(1)   # do whatever you want here
            # self.filepath.get() returns the input file path, if you want to save files
            self.c867.SVO(self.mox, True)
            self.c867.SVO(self.moy, True)
        self.start_btn['state'] = tk.NORMAL

        interval = float(self.period.get())
        if interval == 0:
            interval = 0.01
        after_id = root.after(int(interval*60*1000), self.start)
        nb_loop = self.nb_loop.get()
        if nb_loop != '':
            if self.nb != int(nb_loop):
                self.nb += 1
            else:
                root.after_cancel(after_id)

    def update_position_list(self, pos_list):
        for i, pos in enumerate(pos_list):
            first = 3
            last = pos.find(":")
            pos = pos[:first+1] + str(i+1) + ":" + pos[last+1:]
            self.position_list[i] = pos
        self.pos_list.set(self.position_list)

    def get_current_position(self):
        pos_dict = {}
        piezo_pos = [self.e518.qPOS(self.x)[self.x],
                     self.e518.qPOS(self.y)[self.y],
                     self.e518.qPOS(self.z)[self.z]]
        motor_pos = [self.c867.qPOS(self.mox)[self.mox],
                     self.c867.qPOS(self.moy)[self.moy]]
        pos_dict['piezo'] = piezo_pos
        pos_dict['motor'] = motor_pos
        return pos_dict

    def get_formatted_position(self, index, motor=None, piezo=None):
        if motor is None and piezo is None:
            pos_dict = self.get_current_position()
            piezo = pos_dict['piezo']
            motor = pos_dict['motor']
        space = 20
        white_space = ' '*(space-len(str(motor).replace('-', '')))
        first = f' Pos{index + 1}: Motor: {motor}{white_space}'
        second = f'/ Piezo: {piezo}'
        pos = first + second
        return pos

    @staticmethod
    def get_valid_position(pos):
        position_dic = {}
        index1 = pos.index('Motor: ') + 7
        index2 = pos.index('/')
        motor_coord = eval(pos[index1:index2])
        piezo_coord = eval(pos[index2+9:])
        position_dic['motor'] = motor_coord
        position_dic['piezo'] = piezo_coord
        return position_dic

    def save(self):
        filename = filedialog.asksaveasfilename(initialdir="/", title="Save file")
        if filename.find('txt') == -1:
            filename = filename + '.txt'
        if filename.split('.')[-1] == 'txt':
            with open(filename, 'w') as w:
                content = self.position_list
                cont = '\n' + str([self.pre_ref, self.cur_ref])
                w.write(str(content)+cont)

    def load(self):
        file_open_dia = filedialog.askopenfilename(initialdir="/", title="Select file")
        if file_open_dia.split('.')[-1] == 'txt':
            self.params_load(file_open_dia)

    def params_load(self, file_open_dia):
        with open(file_open_dia, 'r') as r:
            content = r.read().splitlines()
        self.position_list = eval(content[0])
        self.pos_list.set(self.position_list)
        ref_pos = eval(content[1])
        self.pre_ref = ref_pos[0]
        self.cur_ref = ref_pos[1]
        if self.pre_ref == '':
            self.pre_ref = self.cur_ref
        self.ref_position.set(str(self.cur_ref))

    def move(self, motor, piezo):
        self.c867.VEL(self.mox, 0.05)
        self.c867.VEL(self.moy, 0.05)
        self.c867.MOV(self.mox, motor[0])
        self.c867.MOV(self.moy, motor[1])
        pitools.waitontarget(self.c867)
        self.e518.MOV(self.x, piezo[0])
        self.e518.MOV(self.y, piezo[1])
        self.e518.MOV(self.z, piezo[2])
        pitools.waitontarget(self.e518)


class JoyStick(tk.Frame):

    def __init__(self, root, stage):
        self.stage = stage
        self.x = self.stage.axes[1]
        self.y = self.stage.axes[0]
        self.x_range = [self.stage.qTMN(self.x)[self.x], self.stage.qTMX(self.x)[self.x]]
        self.y_range = [self.stage.qTMN(self.y)[self.y], self.stage.qTMX(self.y)[self.y]]
        self.nb_axis = len(self.stage.axes)
        if self.nb_axis == 3:
            self.z = self.stage.axes[2]
        if self.stage.HasHIN():
            self.stage.HIN(self.x, False)
            self.stage.HIN(self.y, False)

        self.popup_win = tk.Toplevel(root)
        dev = self.stage.devname.split('.')[0]
        self.popup_win.wm_title(f"{dev}  Controller")
        self.popup_win.geometry('320x320')
        self.popup_win.configure(bg='white')
        self.popup_win.resizable(0, 0)
        self.popup_win.update()
        self.wn_size = self.popup_win.winfo_width()
        self.wn_pos = [self.popup_win.winfo_rootx(), self.popup_win.winfo_rooty()]
        self.radius = 110
        pad = 200
        self.canvas_range = tk.Canvas(self.popup_win,
                                      bg='white',
                                      borderwidth=0,
                                      highlightthickness=0)
        range_pos = (self.wn_size - (self.radius + pad)) * 0.5
        range_size = (self.radius + pad)
        relsize = range_size / self.wn_size
        self.canvas_range.place(x=range_pos, y=range_pos, relwidth=relsize, relheight=relsize)
        self.create_circle(range_size // 2, range_size // 2, self.radius, self.canvas_range, None)

        if self.nb_axis == 3:
            self.canvas_range.bind('<Enter>', self.bound_to_mousewheel)
            self.canvas_range.bind('<Leave>', self.unbound_to_mousewheel)

        self.dot = tk.Canvas(self.canvas_range,
                             bg='white',
                             borderwidth=0,
                             highlightthickness=0)
        size_ratio = 3
        dot_size = range_size / size_ratio
        self.dot_pos = (range_size - dot_size) * 0.5
        self.dot.place(x=self.dot_pos, y=self.dot_pos, relwidth=1 / size_ratio, relheight=1 / size_ratio)
        self.create_circle(dot_size // 2, dot_size // 2, dot_size * 0.8 // 2, self.dot, 'black')
        self.dot.bind("<Motion>", self.mouse_appearance)
        self.dot.bind("<B1-Motion>", self.drag)
        self.dot.bind("<ButtonRelease-1>", self.centralize)
        self.offset = dot_size - range_pos - dot_size * 0.2 * 2

        self.generator = 0
        self.pressed = False
        self.increment_x = 0
        self.increment_y = 0

    @staticmethod
    def create_circle(x, y, r, canvas, fill):  # center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return canvas.create_oval(x0, y0, x1, y1, outline='black', width=2, fill=fill)

    def bound_to_mousewheel(self, event):
        self.canvas_range.bind("<MouseWheel>", self.set_piezo_axis)

    def unbound_to_mousewheel(self, event):
        self.canvas_range.unbind("<MouseWheel>")

    def drag(self, event):
        self.pressed = True
        if self.generator == 0:
            self.set_stage()
        cur_wn_pos = [self.popup_win.winfo_rootx(), self.popup_win.winfo_rooty()]
        if cur_wn_pos != self.wn_pos:
            self.wn_pos = cur_wn_pos
        x = event.widget.winfo_pointerx() - self.wn_pos[0] - self.offset
        y = event.widget.winfo_pointery() - self.wn_pos[1] - self.offset
        x, y = self.get_coord(x, y)
        event.widget.place(x=x, y=y)

    def mouse_appearance(self, event):
        self.dot.config(cursor="hand2")

    def centralize(self, event):
        self.pressed = False
        self.dot.place(x=self.dot_pos, y=self.dot_pos)

    def get_coord(self, x, y):
        delta_x = self.dot_pos - x
        delta_y = self.dot_pos - y
        radius = (delta_x ** 2 + delta_y ** 2) ** 0.5
        ratio = radius / self.radius
        if ratio <= 1:
            self.increment_x = (x - self.dot_pos) / self.radius
            self.increment_y = (self.dot_pos - y) / self.radius
            return x, y
        else:
            if delta_x < 0:
                edge_x = abs(delta_x / ratio) + self.dot_pos
            else:
                edge_x = self.dot_pos - (delta_x / ratio)
            if delta_y < 0:
                edge_y = abs(delta_y / ratio) + self.dot_pos
            else:
                edge_y = self.dot_pos - (delta_y / ratio)
            self.increment_x = (edge_x - self.dot_pos) / self.radius
            self.increment_y = (self.dot_pos - edge_y) / self.radius
            return edge_x, edge_y

    def set_stage(self):
        cur_pos = [self.stage.qPOS(self.x)[self.x],
                   self.stage.qPOS(self.y)[self.y]]
        self.generator = 0
        if self.pressed:
            if self.nb_axis == 3:
                increment_x = -self.increment_x
                increment_y = -self.increment_y
                unit_x = unit_y = self.stage.qVEL(self.x)[self.x] * 4
            else:
                increment_x = self.increment_x
                increment_y = self.increment_y
                unit_x = 0.02 * (1 + abs(increment_x))
                unit_y = 0.02 * (1 + abs(increment_y))
                self.stage.VEL(self.x, unit_x * abs(increment_x))
                self.stage.VEL(self.y, unit_y * abs(increment_y))
            target_x = cur_pos[0] + unit_x * increment_x
            target_y = cur_pos[1] + unit_y * increment_y
            if self.x_range[0] < target_x < self.x_range[1]:
                self.stage.MOV(self.x, target_x)
            if self.y_range[0] < target_y < self.y_range[1]:
                self.stage.MOV(self.y, target_y)
            self.generator = root.after(10, self.set_stage)
        else:
            if self.generator != 0:
                root.after_cancel(self.generator)

    def set_piezo_axis(self, event):
        cur_z = self.stage.qPOS(self.z)[self.z]
        target_z = cur_z + event.delta / 1200
        self.stage.MOV(self.z, target_z)


class Main(tk.Frame):

    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        popup_win = tk.Toplevel(root)
        popup_win.wm_title("JoyStick Control")
        popup_win.geometry('350x200')
        popup_win.configure(bg='white')
        popup_win.resizable(0, 0)

        sn_label_1 = tk.Label(popup_win, text='C867 Serial Number:',
                              bg='white', font='Arial 12', )
        sn_label_1.place(relx=0.05, rely=0.2)
        self.sn_entry_1 = tk.Entry(popup_win, width=20)
        self.sn_entry_1.insert(0, '0120027194')
        self.sn_entry_1.place(relx=0.5, rely=0.22)

        sn_label_2 = tk.Label(popup_win, text='E518 Serial Number:',
                              bg='white', font='Arial 12', )
        sn_label_2.place(relx=0.05, rely=0.5)
        self.sn_entry_2 = tk.Entry(popup_win, width=20)
        self.sn_entry_2.insert(0, '120027848')
        self.sn_entry_2.place(relx=0.5, rely=0.52)

        enter_btn = tk.Button(popup_win, text='Enter',
                              font='Arial 12', width=12,
                              command=lambda: [self.get_joystick(),
                                               popup_win.destroy()])
        enter_btn.place(relx=0.52, rely=0.78)

        popup_win.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

    def get_joystick(self):
        sn_1 = self.sn_entry_1.get()
        sn_2 = self.sn_entry_2.get()
        c867 = GCSDevice()
        c867.ConnectUSB(serialnum=sn_1)
        print('connected: {}'.format(c867.qIDN().strip()))
        pitools.startup(c867, stages=None, refmodes=None)
        JoyStick(root, c867)

        e518 = GCSDevice()
        e518.ConnectUSB(serialnum=sn_2)
        print('connected: {}'.format(e518.qIDN().strip()))
        pitools.startup(e518, stages=None, refmodes=None)
        JoyStick(root, e518)

        PositionList(root, c867, e518)


if __name__ == '__main__':
    root = tk.Tk()
    root.iconify()
    Main(root)
    root.mainloop()
