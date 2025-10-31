import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("HPhoto-Editor")
        self.root.geometry("800x600")
        
        self.image_path = None
        self.image = None
        self.img_display = None

        self.brightness = tk.DoubleVar(value=1.0)
        self.contrast = tk.DoubleVar(value=1.0)
        self.blur = tk.DoubleVar(value=0.0)
        self.saturation = tk.DoubleVar(value=1.0)

        menu = tk.Menu(root)
        root.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        self.canvas = tk.Canvas(root, bg='gray')
        self.canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        controls = tk.Frame(root, width=800)
        controls.pack(side=tk.LEFT, fill=tk.Y)
        
        self.brightness_button = tk.Button(controls, text="🔆", command=self.adjust_brightness)
        self.brightness_button.pack(pady=5)

        self.contrast_button = tk.Button(controls, text="🔳", command=self.adjust_contrast)
        self.contrast_button.pack(pady=5)
        
        self.blur_button = tk.Button(controls, text="🌫️", command=self.adjust_blur)
        self.blur_button.pack(pady=5)
        
        self.saturation_button = tk.Button(controls, text="🎨", command=self.adjust_saturation)
        self.saturation_button.pack(pady=5)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if file_path:
            self.image_path = file_path
            self.image = Image.open(file_path)
            self.display_image()

    def save_image(self):
        if self.image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("BMP Files", "*.bmp")])
            if file_path:
                self.image.save(file_path)
                messagebox.showinfo("Image Saved", f"Image saved as {file_path}")

    def display_image(self):
        if self.image:
            self.img_display = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, image=self.img_display, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def update_image(self, event=None):
        if self.image:
            img = self.image.copy()
            
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(self.brightness.get())
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(self.contrast.get())
            
            img = img.filter(ImageFilter.GaussianBlur(self.blur.get()))
            
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(self.saturation.get())

            self.img_display = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.img_display, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def adjust_brightness(self):
        self.show_adjust_window("Brightness", self.brightness, 0.5, 1.5)

    def adjust_contrast(self):
        self.show_adjust_window("Contrast", self.contrast, 0.5, 1.5)

    def adjust_blur(self):
        self.show_adjust_window("Blur", self.blur, 0, 5)
    
    def adjust_saturation(self):
        self.show_adjust_window("Saturation", self.saturation, 0.0, 2.0)

    def show_adjust_window(self, title, variable, from_, to):
        window = tk.Toplevel(self.root)
        window.title(title)
        
        tk.Label(window, text=title).pack(pady=10)
        slider = ttk.Scale(window, from_=from_, to=to, orient=tk.HORIZONTAL, variable=variable, command=self.update_image)
        slider.set(variable.get())
        slider.pack(padx=100, pady=10)
        
        button = tk.Button(window, text="Close", command=window.destroy)
        button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoEditor(root)
    root.mainloop()
