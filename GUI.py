# GUI.py

import tkinter as tk
from tkinter import Frame, Text, Scrollbar
import subprocess
from PIL import Image, ImageTk

class MovieOkeApp:
    CONSOLE_WIDTH = 100
    CONSOLE_HEIGHT = 20

    def __init__(self, root):
        self.root = root
        self.console_frame = None
        self.console_process = None
        self.current_frame = None
        self.bg_color = "#000000"
        self.text_color = "#373737"
        self.hover_color = "#FFFFFF"
        self.button_area_color = "#1f1f1f"
        self.icon_size = (40, 40)
        self.icons = [
            Image.open("Generate.png").resize(self.icon_size),
            Image.open("Studio.png").resize(self.icon_size),
            Image.open("Uploads.png").resize(self.icon_size),
            Image.open("DMs.png").resize(self.icon_size),
            Image.open("Store.png").resize(self.icon_size),
            Image.open("Updates.png").resize(self.icon_size),
            Image.open("Placeholder.png").resize(self.icon_size),
        ]
        self.tk_icons = [ImageTk.PhotoImage(icon) for icon in self.icons]
        self.initialize_ui()

    def run_command(self, command, console_output):
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
            console_output.config(state=tk.NORMAL)
            console_output.delete('1.0', tk.END)
            console_output.insert(tk.END, result.stdout)
        except subprocess.CalledProcessError as e:
            console_output.insert(tk.END, f"Error: {e}")
        finally:
            console_output.config(state=tk.DISABLED)

    def run_python_script(self, script_path, console_output):
        try:
            result = subprocess.run(['F.py', script_path], stdout=subprocess.PIPE, text=True, check=True)
            console_output.config(state=tk.NORMAL)
            console_output.delete('1.0', tk.END)
            console_output.insert(tk.END, result.stdout)
        except subprocess.CalledProcessError as e:
            console_output.insert(tk.END, f"Error: {e}")
        finally:
            console_output.config(state=tk.DISABLED)

    def on_hover(self, event):
        event.widget.config(bg=self.hover_color, fg=self.button_area_color)

    def on_leave(self, event):
        event.widget.config(bg=self.button_area_color, fg=self.text_color)

    def create_button(self, frame, text, image, command, side):
        button = tk.Button(
            frame, text=text, image=image, compound="top",
            bg=self.button_area_color, fg=self.text_color, bd=0, highlightthickness=0,
            command=command, activebackground=self.hover_color
        )
        button.bind("<Enter>", self.on_hover)
        button.bind("<Leave>", self.on_leave)
        button.pack(side=side, padx=10, pady=10, anchor="se")
        return button

    def stop_console(self):
        if self.console_process and self.console_process.poll() is None:
            self.console_process.terminate()

    def open_console(self, frame, width, height):
        console_output = Text(frame, wrap=tk.WORD, bg=self.bg_color, fg=self.text_color, height=height, width=width)
        console_output.pack(expand=True, fill=tk.BOTH)

        scrollbar = Scrollbar(frame, command=console_output.yview, bg=self.bg_color, troughcolor=self.button_area_color)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        console_output.config(yscrollcommand=scrollbar.set, state=tk.DISABLED)

        return console_output

    def close_console(self):
        if self.console_frame:
            self.console_frame.destroy()
            self.console_frame = None
        self.stop_console()
        self.console_process = None

    def open_console_tab(self, button_id):
        self.close_console()

        if self.current_frame:
            self.current_frame.destroy()

        self.console_frame = Frame(self.root, bg=self.bg_color)
        self.console_frame.place(relx=0.25, rely=0.25, relwidth=0.5, relheight=0.5, anchor="center")

        console_output = self.open_console(self.console_frame, width=self.CONSOLE_WIDTH, height=self.CONSOLE_HEIGHT)

        if button_id == 1:
            self.run_python_script('F.py', console_output)
        elif button_id == 2:
            self.run_python_script('F.py', console_output)
        elif button_id == 3:
            self.run_python_script('F.py', console_output)
        elif button_id == 4:
            self.run_python_script('F.py', console_output)
        elif button_id == 5:
            self.run_python_script('F.py', console_output)

        self.current_frame = self.console_frame

    def open_about_tab(self):
        self.close_console()
        if self.current_frame:
            self.current_frame.destroy()

        about_frame = Frame(self.root, bg=self.bg_color)
        about_frame.place(relx=0.5, rely=0.5, anchor="center")
        console_output = self.open_console(about_frame, width=self.CONSOLE_WIDTH, height=self.CONSOLE_HEIGHT)

    def initialize_ui(self):
        self.root.title("MovieOke - Unofficial")
        self.root.configure(bg=self.bg_color)
        button_frame = tk.Frame(self.root, bg=self.button_area_color)
        button_frame.pack(side="bottom", fill=tk.X)
        button1 = self.create_button(button_frame, "Generate", self.tk_icons[0], lambda: self.open_console_tab(1), side="left")
        button2 = self.create_button(button_frame, "Studio", self.tk_icons[1], lambda: self.open_console_tab(2), side="left")
        button3 = self.create_button(button_frame, "Uploads", self.tk_icons[2], lambda: self.open_console_tab(3), side="left")
        button4 = self.create_button(button_frame, "DMs", self.tk_icons[3], lambda: self.open_console_tab(4), side="left")
        button5 = self.create_button(button_frame, "Store", self.tk_icons[4], lambda: self.open_console_tab(5), side="left")
        button6 = self.create_button(button_frame, "Updates", self.tk_icons[5], lambda: self.open_console_tab(6), side="left")
        text_var = tk.StringVar()
        text_label = tk.Label(self.root, textvariable=text_var, bg=self.bg_color, fg=self.text_color)
        text_label.pack(pady=20)
        self.root.geometry("1500x1500+{}+{}".format(self.root.winfo_screenwidth() // 5 - 288, self.root.winfo_screenheight() - 300))
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieOkeApp(root)
