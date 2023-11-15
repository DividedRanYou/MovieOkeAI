# 3Oke3

# Import the special lib for helping with the code
import MovieBot as MB

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    import random
    import numpy as np
    import imageio
    import cv2
except Exception as e:
    MB.installer()

MB.clear()

def clear():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

class AnimationGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("3Oke3")

        self.bg_color_toggle = tk.BooleanVar(value=False)
        self.bg_color_toggle_checkbox = tk.Checkbutton(master, text="Change Colors Every Second", variable=self.bg_color_toggle)
        self.bg_color_toggle_checkbox.pack()

        self.color_label = tk.Label(master, text="Choose Background Color:")
        self.color_label.pack()

        self.color_entry = tk.Entry(master)
        self.color_entry.insert(0, "#808080")
        self.color_entry.pack()

        self.num_models_label = tk.Label(master, text="Number of Generated 3D Models:")
        self.num_models_label.pack()

        self.num_models_entry = tk.Entry(master)
        self.num_models_entry.insert(0, "5")
        self.num_models_entry.pack()

        self.duration_label = tk.Label(master, text="Duration of Animation (seconds):")
        self.duration_label.pack()

        self.duration_entry = tk.Entry(master)
        self.duration_entry.insert(0, "10")
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

        self.use_external_video_var = tk.BooleanVar(value=False)
        self.use_external_video_checkbox = tk.Checkbutton(master, text="Use External Video Reference", variable=self.use_external_video_var)
        self.use_external_video_checkbox.pack()

        self.select_external_video_button = tk.Button(master, text="Select External Video", command=self.load_external_video)
        self.select_external_video_button.pack()

        self.generate_button = tk.Button(master, text="Generate Animation", command=self.generate_animation)
        self.generate_button.pack()

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(master, variable=self.progress_var, maximum=100)
        self.progress_bar.pack()

        self.progress_value = 0

    def load_models(self):
        self.obj_files = []  
        self.mtl_files = []
        
        user_obj_files = filedialog.askopenfilenames(title="Select .obj Files", filetypes=[("Wavefront OBJ files", "*.obj")])
        user_mtl_files = filedialog.askopenfilenames(title="Select .mtl Files", filetypes=[("MTL files", "*.mtl")])
        
        if user_obj_files:
            self.obj_files = user_obj_files
        if user_mtl_files:
            self.mtl_files = user_mtl_files

    def load_external_video(self):
        video_extensions = ["mp4", "mov", "avi", "mkv"]
        uti_filetypes = [f"placeholder_for_{ext}" for ext in video_extensions]
        filetypes = [("Video files", uti_filetypes), ("All files", "*.*")]

        self.external_video_file = filedialog.askopenfilename(
            title="Select External Video File",
            filetypes=filetypes
        )

    def generate_animation(self):
        if not hasattr(self, 'obj_files') or not hasattr(self, 'mtl_files'):
            for _ in range(int(self.num_models_entry.get())):
                glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                model_vertices = self.generate_random_model()
                self.draw_model(model_vertices)
        else:
            for _ in range(int(self.num_models_entry.get())):
                glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                model_vertices = self.load_random_model()
                self.draw_model(model_vertices)

        num_frames = int(float(self.duration_entry.get()) * 60)
        self.frame_duration = 1 / 60
        output_filename = self.output_filename_entry.get() + self.output_extension_var.get()

        Render.init()
        width, height = 800, 600
        Render.display.set_mode((width, height), DOUBLEBUF | OPENGL)

        frames = []

        for frame in range(num_frames):
            clear()

            if self.bg_color_toggle.get():
                self.generate_background_color(frame)

            if not hasattr(self, 'obj_files') or not hasattr(self, 'mtl_files'):
                for _ in range(int(self.num_models_entry.get())):
                    glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                    model_vertices = self.generate_random_model()
                    self.draw_model(model_vertices)
            else:
                for _ in range(int(self.num_models_entry.get())):
                    glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                    model_vertices = self.load_random_model()
                    self.draw_model(model_vertices)

            data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
            image = Render.image.fromstring(data, (width, height), 'RGB')
            frame_surface = Render.surfarray.array3d(image)
            frames.append(frame_surface)

            Render.display.flip()
            Render.time.wait(int(self.frame_duration * 1000))

            self.progress_value = (frame + 1) / num_frames * 100
            self.progress_var.set(self.progress_value)
            self.master.update_idletasks()

        if self.use_external_video_var.get() and hasattr(self, 'external_video_file'):
            self.mimic_external_video()

        imageio.mimsave(output_filename, frames, fps=1 / self.frame_duration)
        Render.quit()

        self.progress_var.set(0)

    def generate_background_color(self, frame):
        if frame % 60 == 0:
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

    def mimic_external_video(self):
        external_frames = self.load_external_video_frames()

        if hasattr(self, 'obj_files') and hasattr(self, 'mtl_files'):
            loaded_models = True
        else:
            loaded_models = False

        for frame_surface in external_frames:
            clear()

            if self.bg_color_toggle.get():
                self.generate_background_color(0)

            if loaded_models:
                for _ in range(int(self.num_models_entry.get())):
                    glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                    model_vertices = self.load_random_model()
                    self.draw_model(model_vertices)
            else:
                for _ in range(int(self.num_models_entry.get())):
                    glTranslatef(random.uniform(-0.1, 0.1), random.uniform(-0.1, 0.1), 0.0)
                    model_vertices = self.generate_random_model()
                    self.draw_model(model_vertices)

            Render.display.flip()
            Render.time.wait(int(self.frame_duration * 1000))

            self.progress_value += 1
            self.progress_var.set(self.progress_value)
            self.master.update_idletasks()

    def load_external_video_frames(self):
        video_cap = cv2.VideoCapture(self.external_video_file)
        frames = []
        while True:
            ret, frame = video_cap.read()
            if not ret:
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)
        video_cap.release()
        return frames
    
    def generate_random_model(self):
        num_vertices = 100
        min_range, max_range = -1.0, 1.0

        vertices = []
        for _ in range(num_vertices):
            vertex = [random.uniform(min_range, max_range) for _ in range(3)]
            vertices.append(vertex)

        return vertices

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

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimationGenerator(root)
    root.mainloop()
