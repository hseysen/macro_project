import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from threading import Thread
from pynput.keyboard import Key, Listener
from pynput.keyboard import Controller as Keyboard
from pynput.mouse import Button
from pynput.mouse import Controller as Mouse
from time import sleep
import pickle
import os

AVAILABLE_KEY_PRESSES = [Key.f1, Key.f2, Key.f3, Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.f10, Key.f11,
                         Key.f12, Key.esc, Key.tab, Key.shift, Key.caps_lock, Key.ctrl_l, Key.cmd, Key.alt_l, Key.space,
                         Key.alt_gr, Key.menu, Key.ctrl_r, Key.left, Key.down, Key.up, Key.right, Key.enter]

KEYSTRING_TO_OBJECT = {
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12,
    "esc": Key.esc,
    "tab": Key.tab,
    "shift": Key.shift,
    "caps_lock": Key.caps_lock,
    "ctrl_l": Key.ctrl_l,
    "ctrl": Key.ctrl_l,
    "windows": Key.cmd,
    "cmd": Key.cmd,
    "alt_l": Key.alt_l,
    "alt": Key.alt_l,
    "space": Key.space,
    "alt_r": Key.alt_gr,
    "menu": Key.menu,
    "ctrl_r": Key.ctrl_r,
    "left": Key.left,
    "right": Key.right,
    "up": Key.up,
    "down": Key.down,
    "enter": Key.enter
}


class Peripherals:
    def __init__(self):
        self.mouse = Mouse()
        self.keyboard = Keyboard()

    def listen(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    def keypress_handler(self, key):
        try:
            if key == KEYSTRING_TO_OBJECT[APP.get_mouse_position_key]:
                x, y = self.mouse.position
                APP.xcoord_entry.delete(0, tk.END)
                APP.xcoord_entry.insert(tk.END, str(x))
                APP.ycoord_entry.delete(0, tk.END)
                APP.ycoord_entry.insert(tk.END, str(y))
            if key == KEYSTRING_TO_OBJECT[APP.start_stop_script_execution_key]:
                APP.start_execution()
        except:
            return

    def on_press(self, key):
        self.keypress_handler(key)

    def on_release(self, key):
        return

    def left_click(self, pos):
        self.mouse.position = pos
        self.mouse.click(Button.left, 1)

    def right_click(self, pos):
        self.mouse.position = pos
        self.mouse.click(Button.right, 1)

    def sendkey(self, key):
        try:
            key = KEYSTRING_TO_OBJECT[key]
        except:
            pass
        self.keyboard.press(key)
        self.keyboard.release(key)


class Action:
    def __init__(self, rep_cnt):
        self.x_coord = "-"
        self.y_coord = "-"
        self.delay = "-"
        self.key_press = "-"
        self.rep_cnt = rep_cnt

    def __repr__(self):
        return f"{self.__class__.__name__} {self.x_coord} {self.y_coord} {self.key_press} {self.delay} {self.rep_cnt}"

    __str__ = __repr__

    def execute(self):
        print("Undefined Execute statement for the action.")


class LeftClick(Action):
    def __init__(self, x_coord, y_coord, delay, rep_cnt):
        super().__init__(rep_cnt)
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.delay = delay

    def execute(self):
        sleep(self.delay / 1000)
        for i in range(self.rep_cnt):
            USER.left_click((self.x_coord, self.y_coord))


class RightClick(Action):
    def __init__(self, x_coord, y_coord, delay, rep_cnt):
        super().__init__(rep_cnt)
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.delay = delay

    def execute(self):
        sleep(self.delay / 1000)
        for i in range(self.rep_cnt):
            USER.right_click((self.x_coord, self.y_coord))


class KeyPress(Action):
    def __init__(self, key_press, delay, rep_cnt):
        super().__init__(rep_cnt)
        self.key_press = key_press
        self.delay = delay

    def execute(self):
        sleep(self.delay / 1000)
        for i in range(self.rep_cnt):
            USER.sendkey(self.key_press)


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure_master()
        self.initialize_widgets()
        self.background_process()

    def configure_master(self):
        self.master.title("Macro Program")
        self.master.iconbitmap("img/logo.ico")
        self.master.geometry("768x576")
        self.master.resizable(False, False)

    def background_process(self):
        if self.current_selected_item == -1:
            self.movedn_buttn.state(["disabled"])
            self.moveup_buttn.state(["disabled"])
            self.delete_buttn.state(["disabled"])
        else:
            self.movedn_buttn.state(["!disabled"])
            self.moveup_buttn.state(["!disabled"])
            self.delete_buttn.state(["!disabled"])

        if os.path.exists("userparams.pickle"):
            self.loadls_buttn.state(["!disabled"])
        else:
            self.loadls_buttn.state(["disabled"])

        self.master.after(200, self.background_process)

    def initialize_widgets(self):
        # Variables
        self.current_selected_item = -1
        self.delete_started = False
        self.acttyp_stvar = tk.StringVar()
        self.keyprs_stvar = tk.StringVar()
        self.acttyp_menux = ("Choose an Action", "Left Click", "Right Click", "Key Press")
        self.treevw_clmns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.action_list = []
        self.get_mouse_position_key = None
        self.start_stop_script_execution_key = None

        # Frames
        self.top_frame = ttk.LabelFrame(self.master, text="Add / Edit Action")
        self.mid_frame = ttk.LabelFrame(self.master, text="List of Action(s) to Execute in Sequence")
        self.bot_frame = ttk.LabelFrame(self.master, text="Configurable Global Shortcut Keys for this Script")

        self.top_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.23)
        self.mid_frame.place(relx=0.01, rely=0.25, relwidth=0.98, relheight=0.5)
        self.bot_frame.place(relx=0.01, rely=0.76, relwidth=0.98, relheight=0.23)

        # Top Frame
        self.xcoord_label = ttk.Label(self.top_frame, text="X Co-ordinate :")
        self.ycoord_label = ttk.Label(self.top_frame, text="Y Co-ordinate :")
        self.xcoord_entry = ttk.Entry(self.top_frame)
        self.ycoord_entry = ttk.Entry(self.top_frame)
        self.acttyp_label = ttk.Label(self.top_frame, text="Action Type :")
        self.acttyp_optmn = ttk.OptionMenu(self.top_frame, self.acttyp_stvar, *self.acttyp_menux)
        self.keyprs_label = ttk.Label(self.top_frame, text="Key :")
        self.keyprs_entry = ttk.Entry(self.top_frame)
        self.adelay_label = ttk.Label(self.top_frame, text="Delay before Action :")
        self.adelay_entry = ttk.Entry(self.top_frame)
        self.adelms_label = ttk.Label(self.top_frame, text="Millisecond(s)")
        self.repcnt_label = ttk.Label(self.top_frame, text="Repeat Count :")
        self.repcnt_entry = ttk.Entry(self.top_frame)
        self.addact_buttn = ttk.Button(self.top_frame, text="Add", command=self.add_action)
        self.resact_buttn = ttk.Button(self.top_frame, text="Reset", command=self.reset_action)
        self.loadls_buttn = ttk.Button(self.top_frame, text="Load", command=self.load_params)
        self.savels_buttn = ttk.Button(self.top_frame, text="Save", command=self.save_params)

        self.xcoord_label.place(relx=0.02, rely=0.04)
        self.ycoord_label.place(relx=0.25, rely=0.04)
        self.xcoord_entry.place(relx=0.15, rely=0.04, relwidth=0.08)
        self.ycoord_entry.place(relx=0.38, rely=0.04, relwidth=0.08)
        self.acttyp_label.place(relx=0.02, rely=0.28)
        self.acttyp_optmn.place(relx=0.14, rely=0.28)
        self.keyprs_label.place(relx=0.35, rely=0.28)
        self.keyprs_entry.place(relx=0.40, rely=0.28, relwidth=0.12)
        self.adelay_label.place(relx=0.02, rely=0.52)
        self.adelay_entry.place(relx=0.19, rely=0.52, relwidth=0.08)
        self.adelms_label.place(relx=0.29, rely=0.52)
        self.repcnt_label.place(relx=0.02, rely=0.76)
        self.repcnt_entry.place(relx=0.145, rely=0.76, relwidth=0.08)
        self.addact_buttn.place(relx=0.56, rely=0.04, relwidth=0.2, relheight=0.4)
        self.resact_buttn.place(relx=0.56, rely=0.51, relwidth=0.2, relheight=0.4)
        self.loadls_buttn.place(relx=0.78, rely=0.04, relwidth=0.2, relheight=0.4)
        self.savels_buttn.place(relx=0.78, rely=0.51, relwidth=0.2, relheight=0.4)

        # Mid Frame
        self.action_treev = ttk.Treeview(self.mid_frame, columns=self.treevw_clmns, show="headings", selectmode="browse")
        self.starts_buttn = ttk.Button(self.mid_frame, text="Start", command=self.start_execution)
        self.moveup_buttn = ttk.Button(self.mid_frame, text="Move Up", command=self.move_up)
        self.movedn_buttn = ttk.Button(self.mid_frame, text="Move Down", command=self.move_down)
        self.delete_buttn = ttk.Button(self.mid_frame, text="Delete", command=self.delete_action)

        self.action_treev.place(relx=0.02, rely=0.02, relwidth=0.74, relheight=0.95)
        self.starts_buttn.place(relx=0.78, rely=0.03, relwidth=0.2, relheight=0.2)
        self.moveup_buttn.place(relx=0.78, rely=0.275, relwidth=0.2, relheight=0.2)
        self.movedn_buttn.place(relx=0.78, rely=0.52, relwidth=0.2, relheight=0.2)
        self.delete_buttn.place(relx=0.78, rely=0.765, relwidth=0.2, relheight=0.2)

        # Bottom Frame
        self.getmsp_label = ttk.Label(self.bot_frame, text="Get Mouse Position :", anchor=tk.E)
        self.getmsp_entry = ttk.Entry(self.bot_frame)
        self.getasn_buttn = ttk.Button(self.bot_frame, text="Assign", command=self.assign_btn_1)
        self.getclr_buttn = ttk.Button(self.bot_frame, text="Clear", command=self.clear_btn_1)
        self.strstp_label = ttk.Label(self.bot_frame, text="Start / Stop Script Execution :", anchor=tk.E)
        self.strstp_entry = ttk.Entry(self.bot_frame)
        self.strasn_buttn = ttk.Button(self.bot_frame, text="Assign", command=self.assign_btn_2)
        self.strclr_buttn = ttk.Button(self.bot_frame, text="Clear", command=self.clear_btn_2)

        self.getmsp_label.place(relx=0, rely=0.27, relwidth=0.32)
        self.getmsp_entry.place(relx=0.34, rely=0.27, relwidth=0.25)
        self.getasn_buttn.place(relx=0.62, rely=0.26, relwidth=0.12, relheight=0.21)
        self.getclr_buttn.place(relx=0.75, rely=0.26, relwidth=0.12, relheight=0.21)
        self.strstp_label.place(relx=0, rely=0.53, relwidth=0.32)
        self.strstp_entry.place(relx=0.34, rely=0.53, relwidth=0.25)
        self.strasn_buttn.place(relx=0.62, rely=0.52, relwidth=0.12, relheight=0.21)
        self.strclr_buttn.place(relx=0.75, rely=0.52, relwidth=0.12, relheight=0.21)

        # Treeview Headings and Columns
        self.action_treev.heading("#1", text="Action Type")
        self.action_treev.heading("#2", text="X")
        self.action_treev.heading("#3", text="Y")
        self.action_treev.heading("#4", text="Key")
        self.action_treev.heading("#5", text="Delay")
        self.action_treev.heading("#6", text="Repeats")

        self.action_treev.column("#1", width=100, stretch=False)
        self.action_treev.column("#2", width=50, stretch=False)
        self.action_treev.column("#3", width=50, stretch=False)
        self.action_treev.column("#4", width=90, stretch=False)
        self.action_treev.column("#5", width=90, stretch=False)
        self.action_treev.column("#6", width=60, stretch=False)

        # Treeview binds
        self.action_treev.bind("<Button-1>", self.prevent_resize)
        self.action_treev.bind("<Motion>", self.prevent_resize)
        self.action_treev.bind("<<TreeviewSelect>>", self.item_selected)

        # Scroll Bar
        self.action_scrll = ttk.Scrollbar(self.mid_frame, orient=tk.VERTICAL, command=self.action_treev.yview)
        self.action_treev.configure(yscroll=self.action_scrll.set)
        self.action_scrll.place(relx=0.76, rely=0.02, relwidth=0.02, relheight=0.95)

    def add_action(self):
        if self.acttyp_stvar.get() == "Choose an Action":
            messagebox.showerror(title="No Action Type Selected",
                                 message="Please choose an Action Type!")
            return

        obj = None

        if self.acttyp_stvar.get() == "Left Click" or self.acttyp_stvar.get() == "Right Click":
            try:
                x = int(self.xcoord_entry.get())
                y = int(self.ycoord_entry.get())
                d = int(self.adelay_entry.get())
                r = int(self.repcnt_entry.get())

                if self.acttyp_stvar.get() == "Left Click":
                    obj = LeftClick(x, y, d, r)
                else:
                    obj = RightClick(x, y, d, r)

            except Exception:
                messagebox.showerror(title="Invalid Click Parameters",
                                     message="Please provide the coordinates, delay and repeat count of the Click!")
                return

        if self.acttyp_stvar.get() == "Key Press":
            try:
                obj = KeyPress(self.keyprs_entry.get(), int(self.adelay_entry.get()), int(self.repcnt_entry.get()))
            except Exception:
                messagebox.showerror(title="Invalid Key Press Parameters",
                                     message="Please provide the delay and repeat count of the Key Press!")
                return

        if obj is None:
            messagebox.showerror(title="Unexpected Error",
                                 message="Something unexpected happened. Please make sure everything is right.")
            return

        self.add_object_to_action(obj)

    def add_object_to_action(self, obj):
        self.action_list.append(obj)
        self.action_treev.insert('', tk.END, values=str(obj))

    def reset_action(self):
        self.acttyp_stvar.set("")
        self.acttyp_optmn = ttk.OptionMenu(self.top_frame, self.acttyp_stvar, *self.acttyp_menux)

        self.xcoord_entry.delete(0, tk.END)
        self.ycoord_entry.delete(0, tk.END)
        self.keyprs_entry.delete(0, tk.END)
        self.adelay_entry.delete(0, tk.END)
        self.repcnt_entry.delete(0, tk.END)

    def start_execution(self):
        for each in self.action_treev.get_children():
            self.action_list[self.action_treev.index(each)].execute()

    def move_up(self):
        row = self.action_treev.selection()[0]
        prev_index = self.action_treev.index(row)
        if prev_index == 0:
            return
        self.action_list[prev_index], self.action_list[prev_index - 1] = self.action_list[prev_index - 1], self.action_list[prev_index]
        self.action_treev.move(row, self.action_treev.parent(row), prev_index - 1)

    def move_down(self):
        row = self.action_treev.selection()[0]
        prev_index = self.action_treev.index(row)
        if prev_index == len(self.action_list) - 1:
            return
        self.action_list[prev_index], self.action_list[prev_index + 1] = self.action_list[prev_index + 1], self.action_list[prev_index]
        self.action_treev.move(row, self.action_treev.parent(row), prev_index + 1)

    def delete_action(self):
        try:
            self.delete_buttn.state(["disabled"])
            self.movedn_buttn.state(["disabled"])
            self.moveup_buttn.state(["disabled"])
            selected_item = self.action_treev.selection()[0]
            self.action_list.pop(self.action_treev.index(selected_item))
            self.action_treev.delete(selected_item)
        except IndexError:
            pass
        finally:
            self.current_selected_item = -1

    def assign_btn_1(self):
        inp = self.getmsp_entry.get()
        try:
            if KEYSTRING_TO_OBJECT[inp.lower()] not in AVAILABLE_KEY_PRESSES:
                messagebox.showerror(title="Invalid Key Assignment",
                                     message="Please provide a valid Key!",
                                     detail=f"Available keys: {list(KEYSTRING_TO_OBJECT.keys())}")
                return
            else:
                self.get_mouse_position_key = inp
        except Exception:
            messagebox.showerror(title="Invalid Key Assignment",
                                 message="Please provide a valid Key!",
                                 detail=f"Available keys:\n{', '.join(list(KEYSTRING_TO_OBJECT.keys()))}")
            return

    def assign_btn_2(self):
        inp = self.strstp_entry.get()
        try:
            if KEYSTRING_TO_OBJECT[inp.lower()] not in AVAILABLE_KEY_PRESSES:
                messagebox.showerror(title="Invalid Key Assignment",
                                     message="Please provide a valid Key!",
                                     detail=f"Available keys: {list(KEYSTRING_TO_OBJECT.keys())}")
                return
            else:
                self.start_stop_script_execution_key = inp
        except Exception:
            messagebox.showerror(title="Invalid Key Assignment",
                                 message="Please provide a valid Key!",
                                 detail=f"Available keys:\n{', '.join(list(KEYSTRING_TO_OBJECT.keys()))}")
            return

    def clear_btn_1(self):
        self.get_mouse_position_key = None
        self.getmsp_entry.delete(0, tk.END)

    def clear_btn_2(self):
        self.start_stop_script_execution_key = None
        self.strstp_entry.delete(0, tk.END)

    def prevent_resize(self, event):
        if self.action_treev.identify_region(event.x, event.y) == "separator":
            return "break"

    def item_selected(self, _):
        for x in self.action_treev.selection():
            self.current_selected_item = x

    def load_params(self):
        with open("userparams.pickle", "rb") as rf:
            params = pickle.load(rf)

        xs = params["actions"]
        self.get_mouse_position_key = params["mouse position key"]
        self.start_stop_script_execution_key = params["start execution key"]

        for obj in xs:
            self.add_object_to_action(obj)

        self.getmsp_entry.delete(0, tk.END)
        self.getmsp_entry.insert(0, self.get_mouse_position_key)
        self.strstp_entry.delete(0, tk.END)
        self.strstp_entry.insert(0, self.start_stop_script_execution_key)

    def save_params(self):
        params = dict()
        params["actions"] = self.action_list
        params["mouse position key"] = self.get_mouse_position_key
        params["start execution key"] = self.start_stop_script_execution_key
        with open("userparams.pickle", "wb") as wf:
            pickle.dump(params, wf)


USER = Peripherals()
APP: Application


def gui_thread():
    global APP
    root = tk.Tk()
    APP = Application(root)
    APP.mainloop()


def user_thread():
    global USER
    USER.listen()


def main():
    g = Thread(target=gui_thread)
    g.start()

    u = Thread(target=user_thread)
    u.start()

    g.join()
    u.join()


if __name__ == "__main__":
    main()
