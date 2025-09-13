import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageOps
import os

class ExamPhotoResizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Government Exam Photo & Signature Resizer")
        self.root.geometry("750x650")
        self.image = None
        self.preview_image = None
        self.presets = self.load_presets()
        self.default_width, self.default_height = self.load_default_dims()
        self.setup_gui()

    def load_presets(self):
        return {
            "TNPSC Group Exams": {
                "Photo": {"width": 276, "height": 354, "min_kb": 20, "max_kb": 50, "dpi": 200},
                "Signature": {"width": 472, "height": 157, "min_kb": 10, "max_kb": 20, "dpi": 200},
                "Other Documents": {"width": 300, "height": 400, "min_kb": 50, "max_kb": 100, "dpi": 200}
            },
            "UPSC/IAS": {
                "Photo": {"width": 350, "height": 350, "min_kb": 20, "max_kb": 300, "dpi": 96},
                "Signature": {"width": 140, "height": 60, "min_kb": 10, "max_kb": 20, "dpi": 96},
                "Other Documents": {"width": 1000, "height": 1000, "min_kb": 50, "max_kb": 300, "dpi": 96}
            },
            "SSC (CGL/CHSL/MTS)": {
                "Photo": {"width": 200, "height": 230, "min_kb": 20, "max_kb": 50, "dpi": 96},
                "Signature": {"width": 140, "height": 60, "min_kb": 10, "max_kb": 20, "dpi": 96},
                "Other Documents": {"width": 300, "height": 400, "min_kb": 50, "max_kb": 100, "dpi": 96}
            },
            "IBPS PO/Clerk/RRB": {
                "Photo": {"width": 200, "height": 230, "min_kb": 20, "max_kb": 50, "dpi": 96},
                "Signature": {"width": 140, "height": 60, "min_kb": 10, "max_kb": 20, "dpi": 96},
                "Other Documents": {"width": 300, "height": 400, "min_kb": 50, "max_kb": 100, "dpi": 96}
            },
            "Railway (RRB NTPC/Group D)": {
                "Photo": {"width": 200, "height": 230, "min_kb": 20, "max_kb": 50, "dpi": 96},
                "Signature": {"width": 140, "height": 60, "min_kb": 10, "max_kb": 20, "dpi": 96},
                "Other Documents": {"width": 300, "height": 400, "min_kb": 50, "max_kb": 100, "dpi": 96}
            }
        }

    def load_default_dims(self):
        default_file = "default_dims.txt"
        if os.path.exists(default_file):
            with open(default_file, 'r') as f:
                lines = f.readlines()
                if len(lines) >= 2:
                    return int(lines[0].strip()), int(lines[1].strip())
        return 276, 354

    def save_default_dims(self, width, height):
        with open("default_dims.txt", 'w') as f:
            f.write(f"{width}\n{height}")

    def cm_to_pixels(self, cm, dpi):
        return int(cm * (dpi / 2.54))

    def setup_gui(self):
        tk.Label(self.root, text="Select Exam:", font=("Arial", 12, "bold")).pack(pady=10)
        self.exam_var = tk.StringVar(value=list(self.presets.keys())[0])
        exam_combo = ttk.Combobox(self.root, textvariable=self.exam_var, values=list(self.presets.keys()), state="readonly")
        exam_combo.pack(pady=5)
        exam_combo.bind("<<ComboboxSelected>>", self.on_exam_change)

        tk.Label(self.root, text="Select Type:", font=("Arial", 12, "bold")).pack(pady=10)
        self.type_var = tk.StringVar(value="Photo")
        type_combo = ttk.Combobox(self.root, textvariable=self.type_var, values=["Photo", "Signature", "Other Documents"], state="readonly")
        type_combo.pack(pady=5)
        type_combo.bind("<<ComboboxSelected>>", self.on_type_change)

        # Custom Dimensions Frame
        dim_frame = ttk.Frame(self.root)
        dim_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(dim_frame, text="Custom Dimensions:", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=5)

        tk.Label(dim_frame, text="Width (px):", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=2)
        self.custom_width_px = tk.Entry(dim_frame, width=10)
        self.custom_width_px.grid(row=1, column=1, padx=5, pady=2)
        self.custom_width_px.insert(0, "Enter in px")
        self.custom_width_px.bind("<FocusIn>", lambda e: self.clear_placeholder(self.custom_width_px, "Enter in px"))
        self.custom_width_px.bind("<FocusOut>", lambda e: self.restore_placeholder(self.custom_width_px, "Enter in px"))

        tk.Label(dim_frame, text="Width (cm):", font=("Arial", 10)).grid(row=1, column=2, padx=5, pady=2)
        self.custom_width_cm = tk.Entry(dim_frame, width=10)
        self.custom_width_cm.grid(row=1, column=3, padx=5, pady=2)
        self.custom_width_cm.insert(0, "Enter in cm")
        self.custom_width_cm.bind("<FocusIn>", lambda e: self.clear_placeholder(self.custom_width_cm, "Enter in cm"))
        self.custom_width_cm.bind("<FocusOut>", lambda e: self.restore_placeholder(self.custom_width_cm, "Enter in cm"))

        tk.Label(dim_frame, text="Height (px):", font=("Arial", 10)).grid(row=2, column=0, padx=5, pady=2)
        self.custom_height_px = tk.Entry(dim_frame, width=10)
        self.custom_height_px.grid(row=2, column=1, padx=5, pady=2)
        self.custom_height_px.insert(0, "Enter in px")
        self.custom_height_px.bind("<FocusIn>", lambda e: self.clear_placeholder(self.custom_height_px, "Enter in px"))
        self.custom_height_px.bind("<FocusOut>", lambda e: self.restore_placeholder(self.custom_height_px, "Enter in px"))

        tk.Label(dim_frame, text="Height (cm):", font=("Arial", 10)).grid(row=2, column=2, padx=5, pady=2)
        self.custom_height_cm = tk.Entry(dim_frame, width=10)
        self.custom_height_cm.grid(row=2, column=3, padx=5, pady=2)
        self.custom_height_cm.insert(0, "Enter in cm")
        self.custom_height_cm.bind("<FocusIn>", lambda e: self.clear_placeholder(self.custom_height_cm, "Enter in cm"))
        self.custom_height_cm.bind("<FocusOut>", lambda e: self.restore_placeholder(self.custom_height_cm, "Enter in cm"))

        tk.Button(dim_frame, text="Save as Default", command=self.save_default, bg="lightyellow").grid(row=3, column=0, columnspan=4, pady=10)

        tk.Label(self.root, text="Target File Size (KB, e.g., 47, leave blank for preset):", font=("Arial", 10, "bold")).pack(pady=10)
        self.size_entry = tk.Entry(self.root, width=10)
        self.size_entry.pack(pady=5)
        self.size_entry.bind("<KeyRelease>", self.on_size_change)

        tk.Button(self.root, text="Load Image", command=self.load_image, bg="lightblue", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Label(self.root, text="Preview:", font=("Arial", 12, "bold")).pack(pady=5)
        self.preview_label = tk.Label(self.root, bg="white", width=50, height=20)
        self.preview_label.pack(pady=5)
        self.specs_label = tk.Label(self.root, text="", justify=tk.LEFT, font=("Arial", 10))
        self.specs_label.pack(pady=5)
        tk.Button(self.root, text="Resize & Compress", command=self.process_image, bg="lightgreen", font=("Arial", 10, "bold")).pack(pady=10)
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 10)).pack(pady=5)

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def restore_placeholder(self, entry, placeholder):
        if not entry.get().strip():
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def save_default(self):
        width_px = self.custom_width_px.get().strip() or str(self.default_width)
        height_px = self.custom_height_px.get().strip() or str(self.default_height)
        try:
            width = int(width_px) if self.custom_width_px.get().strip() and width_px != "Enter in px" else self.cm_to_pixels(float(self.custom_width_cm.get().strip() or 0), self.presets[self.exam_var.get()][self.type_var.get()]['dpi']) if self.custom_width_cm.get().strip() and self.custom_width_cm.get().strip() != "Enter in cm" else self.default_width
            height = int(height_px) if self.custom_height_px.get().strip() and height_px != "Enter in px" else self.cm_to_pixels(float(self.custom_height_cm.get().strip() or 0), self.presets[self.exam_var.get()][self.type_var.get()]['dpi']) if self.custom_height_cm.get().strip() and self.custom_height_cm.get().strip() != "Enter in cm" else self.default_height
            self.default_width, self.default_height = width, height
            self.save_default_dims(width, height)
            messagebox.showinfo("Success", f"Default dimensions saved: {width}x{height} pixels")
            self.update_specs()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid pixel or cm values for default dimensions")

    def load_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if file_path:
            try:
                self.image = Image.open(file_path)
                self.update_preview()
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
                self.update_specs()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")

    def update_preview(self):
        if self.image:
            preview_size = (400, 300)
            self.preview_image = self.image.copy()
            self.preview_image.thumbnail(preview_size, Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(self.preview_image)
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo

    def update_specs(self):
        exam = self.exam_var.get()
        typ = self.type_var.get()
        if exam in self.presets and typ in self.presets[exam]:
            preset = self.presets[exam][typ]
            custom_size = self.size_entry.get().strip()
            size_text = f"{custom_size} KB (custom)" if custom_size else f"{preset['min_kb']}-{preset['max_kb']} KB (preset)"
            custom_w_px = self.custom_width_px.get().strip()
            custom_h_px = self.custom_height_px.get().strip()
            custom_w_cm = self.custom_width_cm.get().strip()
            custom_h_cm = self.custom_height_cm.get().strip()
            if custom_w_px or custom_h_px or custom_w_cm or custom_h_cm:
                dims = []
                if custom_w_px and custom_w_px != "Enter in px" and custom_h_px and custom_h_px != "Enter in px":
                    dims = [f"{custom_w_px}px x {custom_h_px}px"]
                elif custom_w_cm and custom_w_cm != "Enter in cm" and custom_h_cm and custom_h_cm != "Enter in cm":
                    dims = [f"{custom_w_cm}cm x {custom_h_cm}cm"]
                elif custom_w_px and custom_w_px != "Enter in px" or custom_h_px and custom_h_px != "Enter in px":
                    w = custom_w_px if custom_w_px and custom_w_px != "Enter in px" else str(self.cm_to_pixels(float(custom_w_cm or 0), preset['dpi']) if custom_w_cm and custom_w_cm != "Enter in cm" else self.default_width)
                    h = custom_h_px if custom_h_px and custom_h_px != "Enter in px" else str(self.cm_to_pixels(float(custom_h_cm or 0), preset['dpi']) if custom_h_cm and custom_h_cm != "Enter in cm" else self.default_height)
                    dims = [f"{w}px x {h}px"]
                elif custom_w_cm and custom_w_cm != "Enter in cm" or custom_h_cm and custom_h_cm != "Enter in cm":
                    w = custom_w_cm if custom_w_cm and custom_w_cm != "Enter in cm" else str(self.cm_to_pixels(float(self.default_width / (preset['dpi'] / 2.54)), preset['dpi']) / (preset['dpi'] / 2.54))
                    h = custom_h_cm if custom_h_cm and custom_h_cm != "Enter in cm" else str(self.cm_to_pixels(float(self.default_height / (preset['dpi'] / 2.54)), preset['dpi']) / (preset['dpi'] / 2.54))
                    dims = [f"{w}cm x {h}cm"]
                dim_text = ", ".join(dims) + " (Custom)"
            else:
                dim_text = f"{self.default_width}x{self.default_height}px (Default)"
            specs = f"Target: {dim_text}, {size_text}, DPI: {preset['dpi']}"
            self.specs_label.config(text=specs)

    def process_image(self):
        if not self.image:
            messagebox.showerror("Error", "No image loaded!")
            return

        exam = self.exam_var.get()
        typ = self.type_var.get()
        if exam not in self.presets or typ not in self.presets[exam]:
            messagebox.showerror("Error", "Invalid exam or type selected!")
            return

        preset = self.presets[exam][typ]
        dpi = preset['dpi']
        min_size_bytes = preset['min_kb'] * 1024
        max_size_bytes = preset['max_kb'] * 1024

        # Determine dimensions
        custom_w_px = self.custom_width_px.get().strip()
        custom_h_px = self.custom_height_px.get().strip()
        custom_w_cm = self.custom_width_cm.get().strip()
        custom_h_cm = self.custom_height_cm.get().strip()

        if custom_w_px or custom_h_px or custom_w_cm or custom_h_cm:
            try:
                width_px = int(custom_w_px) if custom_w_px and custom_w_px != "Enter in px" else self.cm_to_pixels(float(custom_w_cm or 0), dpi) if custom_w_cm and custom_w_cm != "Enter in cm" else self.default_width
                height_px = int(custom_h_px) if custom_h_px and custom_h_px != "Enter in px" else self.cm_to_pixels(float(custom_h_cm or 0), dpi) if custom_h_cm and custom_h_cm != "Enter in cm" else self.default_height
                if width_px <= 0 or height_px <= 0:
                    raise ValueError("Dimensions must be positive!")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid custom dimensions: {e}")
                return
        else:
            width_px, height_px = self.default_width, self.default_height

        custom_size = self.size_entry.get().strip()
        try:
            target_size_bytes = float(custom_size) * 1024 if custom_size else preset['max_kb'] * 1024
            if target_size_bytes < min_size_bytes or target_size_bytes > max_size_bytes:
                raise ValueError(f"Target size must be between {preset['min_kb']} and {preset['max_kb']} KB!")
            if target_size_bytes <= 0:
                raise ValueError("Target size must be positive!")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid target file size: {e}")
            return

        try:
            resized = self.image.resize((width_px, height_px), Image.Resampling.LANCZOS)
            if typ == "Signature":
                resized = ImageOps.grayscale(resized)

            output_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
            if not output_path:
                return

            input_size_kb = os.path.getsize(self.image.filename) / 1024 if hasattr(self.image, 'filename') else 1500
            pixel_count = width_px * height_px
            est_quality = min(100, max(80, int(100 * (target_size_bytes / (input_size_kb * 0.03)))))

            low, high = 10, 100
            quality = est_quality
            max_iterations = 10
            tolerance = 512
            from io import BytesIO
            best_buffer = None
            best_quality = quality
            best_diff = float('inf')

            for i in range(max_iterations):
                buffer = BytesIO()
                resized.save(buffer, format='JPEG', quality=quality, dpi=(dpi, dpi))
                img_size = len(buffer.getvalue())
                diff = abs(img_size - target_size_bytes)

                if diff < best_diff:
                    best_diff = diff
                    best_buffer = buffer.getvalue()
                    best_quality = quality

                if diff <= tolerance:
                    break

                if img_size > target_size_bytes:
                    high = quality - 2 if quality > 20 else quality - 1
                else:
                    low = quality + 2 if quality < 80 else quality + 1
                quality = (low + high) // 2 if low < high else quality

                if i == max_iterations - 1 and img_size < target_size_bytes and quality < 100:
                    quality += 1

            with open(output_path, 'wb') as f:
                f.write(best_buffer)
            actual_size = os.path.getsize(output_path) / 1024
            if actual_size < min_size_bytes / 1024:
                messagebox.showwarning("Warning", f"Minimum size is {preset['min_kb']} KB. Output is {actual_size:.1f} KB. Use a higher-resolution or more detailed image.")
            self.status_var.set(f"Saved: {os.path.basename(output_path)} ({actual_size:.1f} KB, Quality: {best_quality})")
            messagebox.showinfo("Success", f"Image processed! Size: {actual_size:.1f} KB")
            self.image = Image.open(output_path)
            self.update_preview()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")

    def on_exam_change(self, *args):
        self.update_specs()

    def on_type_change(self, *args):
        self.update_specs()

    def on_size_change(self, *args):
        self.update_specs()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamPhotoResizer(root)
    root.mainloop()