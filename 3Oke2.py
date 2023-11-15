# 3Oke2

# Import the side custom made lib for this code
import MovieBot as MB

# Import all libs and install them if not installed along with pip and upgrade to the latest versions
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import pygame as Render
    from pygame.locals import *
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    import random
    import numpy as np
    import imageio
    from tkinter import ttk
except ImportError:
    MB.installer()

# Clear the screen so its nice and fresh!
MB.clear()

# Create the UI to generate random animations
class AnimationGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("3Oke2")

        self.color_toggle_var = tk.BooleanVar(value=False)  # Default: False
        self.color_toggle = tk.Checkbutton(master, text="Change Colors Every Second", variable=self.color_toggle_var)
        self.color_toggle.pack()

        self.color_label = tk.Label(master, text="Choose Background Color:")
        self.color_label.pack()

        self.color_entry = tk.Entry(master)
        self.color_entry.insert(0, "#808080")  # Default: Grey
        self.color_entry.pack()

        self.num_models_label = tk.Label(master, text="Number of Generated 3D Models:")
        self.num_models_label.pack()

        self.num_models_entry = tk.Entry(master)
        self.num_models_entry.insert(0, "5")
        self.num_models_entry.pack()

        self.duration_label = tk.Label(master, text="Duration of Animation (seconds):")
        self.duration_label.pack()

        self.duration_entry = tk.Entry(master)
        self.duration_entry.insert(0, "10")  # Default: 10 seconds
        self.duration_entry.pack()

        self.output_filename_label = tk.Label(master, text="Output Filename:")
        self.output_filename_label.pack()

        self.output_filename_entry = tk.Entry(master)
        self.output_filename_entry.insert(0, "Generated")
        self.output_filename_entry.pack()

        self.output_extension_label = tk.Label(master, text="Output Video File Extension:")
        self.output_extension_label.pack()

        video_extensions = [".mp4", ".mov", ".avi", ".mkv"]
        self.output_extension_var = tk.StringVar(value=video_extensions[0])
        self.output_extension_menu = tk.OptionMenu(master, self.output_extension_var, *video_extensions)
        self.output_extension_menu.pack()

        self.load_models_button = tk.Button(master, text="Load Models", command=self.load_models)
        self.load_models_button.pack()

        self.generate_button = tk.Button(master, text="Generate Animation", command=self.generate_animation)
        self.generate_button.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(master, variable=self.progress_var, maximum=100)
        self.progress_bar.pack()

    def load_models(self):
        self.obj_files = filedialog.askopenfilenames(title="Select .obj Files", filetypes=[("Wavefront OBJ files", "*.obj")])
        self.mtl_files = filedialog.askopenfilenames(title="Select .mtl Files", filetypes=[("MTL files", "*.mtl")])

    def generate_animation(self):
        if not hasattr(self, 'obj_files') or not hasattr(self, 'mtl_files'):
            messagebox.showerror("Error", "Please load .obj and .mtl files.")
            return

        num_frames = int(float(self.duration_entry.get()) * 60)
        frame_duration = 1 / 60
        output_filename = self.output_filename_entry.get() + self.output_extension_var.get()

        Render.init()
        width, height = 800, 600
        Render.display.set_mode((width, height), DOUBLEBUF | OPENGL)

        frames = []

        for frame in range(num_frames):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            if self.color_toggle_var.get():
                self.generate_background_color(frame)

            for _ in range(int(self.num_models_entry.get())):
                glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                model_vertices = self.load_random_model()
                self.draw_model(model_vertices)

            data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
            image = Render.image.fromstring(data, (width, height), 'RGB')
            frame_surface = Render.surfarray.array3d(image)
            frames.append(frame_surface)

            Render.display.flip()
            Render.time.wait(int(frame_duration * 1000))

            # Update progress bar
            progress_value = (frame + 1) / num_frames * 100
            self.progress_var.set(progress_value)
            self.master.update_idletasks()

        imageio.mimsave(output_filename, frames, fps=1 / frame_duration)
        Render.quit()

        # Reset progress bar
        self.progress_var.set(0)

    def generate_background_color(self, frame):
        if frame % 60 == 0:  # Change color every second
            color_str = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            self.color_entry.delete(0, tk.END)
            self.color_entry.insert(0, color_str)

        color_str = self.color_entry.get()
        try:
            color = [int(color_str[i:i + 2], 16) / 255.0 for i in (1, 3, 5)]
            glClearColor(*color, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        except ValueError:
            messagebox.showerror("Error", "Invalid color format. Use #RRGGBB.")

    def load_random_model(self):
        model_file = random.choice(self.obj_files)
        return self.load_obj(model_file)

    def load_obj(self, filename):
        vertices = []
        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertices.append(list(map(float, line[2:].split())))
        return vertices

    def draw_model(self, vertices):
        glBegin(GL_POINTS)
        for vertex in vertices:
            glVertex3fv(vertex)
        glEnd()

# Startup the tool
if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationGenerator(root)
    root.mainloop()
