import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ftplib import FTP
from io import BytesIO
from PIL import Image, ImageTk

class PS4AppMetaManager:
    def __init__(self, root):
        self.root = root
        self.root.title("PS4 AppMeta Manager - By Mr. Velox")
        self.root.geometry("620x580")
        self.root.resizable(False, False)
        self.config_file = "config.json"
        self.current_image_path = None
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.main_frame = ttk.Frame(self.root, padding="15")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        conn_frame = ttk.LabelFrame(self.main_frame, text="Connection Parameters", padding="15")
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(conn_frame, text="Console IP:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ip_var = tk.StringVar()
        self.ip_entry = ttk.Entry(conn_frame, textvariable=self.ip_var, width=22)
        self.ip_entry.grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(conn_frame, text="FTP Port:").grid(row=0, column=2, sticky=tk.W, padx=(15, 0), pady=5)
        self.port_var = tk.StringVar(value="2121")
        self.port_entry = ttk.Entry(conn_frame, textvariable=self.port_var, width=12)
        self.port_entry.grid(row=0, column=3, padx=10, pady=5)
        
        ttk.Label(conn_frame, text="CUSA ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cusa_var = tk.StringVar()
        self.cusa_entry = ttk.Entry(conn_frame, textvariable=self.cusa_var, width=22)
        self.cusa_entry.grid(row=1, column=1, padx=10, pady=5)
        
        save_btn = ttk.Button(conn_frame, text="Save IP/Port", command=self.save_config)
        save_btn.grid(row=1, column=3, pady=5, sticky=tk.E)
        
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.tab_ext = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_ext, text="External Icon Management")
        
        self.tab_int = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_int, text="Internal Background Management")
        
        self.setup_tab(self.tab_ext, "External", 512, 512, self.process_external, "icon0.png")
        self.setup_tab(self.tab_int, "Internal", 1920, 1080, self.process_internal, "pic0.png & pic1.png")
        
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=2)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_tab(self, parent, mode, w, h, command, target_files):
        container = ttk.Frame(parent, padding="15")
        container.pack(fill=tk.BOTH, expand=True)
        
        header_text = f"Target Dimensions: {w}x{h} px\nTarget Files: {target_files}"
        info_label = ttk.Label(container, text=header_text, justify=tk.CENTER, font=('', 10, 'bold'))
        info_label.pack(pady=(0, 15))
        
        preview_frame = ttk.Frame(container, width=220, height=220, relief=tk.GROOVE)
        preview_frame.pack(pady=10)
        preview_frame.pack_propagate(False)
        
        preview_label = ttk.Label(preview_frame, text="[ Image Preview ]", anchor=tk.CENTER)
        preview_label.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(container)
        btn_frame.pack(pady=20)
        
        select_btn = ttk.Button(btn_frame, text="Load Local Image", command=lambda: self.select_image(preview_label))
        select_btn.pack(side=tk.LEFT, padx=10)
        
        upload_btn = ttk.Button(btn_frame, text=f"Push to PS4 ({mode})", command=command)
        upload_btn.pack(side=tk.LEFT, padx=10)

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    self.ip_var.set(data.get('ip', ''))
                    self.port_var.set(data.get('port', '2121'))
            except Exception:
                pass

    def save_config(self):
        data = {
            'ip': self.ip_var.get(),
            'port': self.port_var.get()
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(data, f)
            self.status_var.set("Configuration metrics saved.")
        except Exception as e:
            messagebox.showerror("I/O Error", str(e))

    def select_image(self, label_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Image Resources", "*.png *.jpg *.jpeg")])
        if file_path:
            self.current_image_path = file_path
            try:
                img = Image.open(file_path)
                img.thumbnail((200, 200))
                photo = ImageTk.PhotoImage(img)
                label_widget.configure(image=photo, text="")
                label_widget.image = photo
                self.status_var.set(f"Loaded payload: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Render Error", str(e))

    def upload_via_ftp(self, size, filenames):
        ip = self.ip_var.get().strip()
        port = self.port_var.get().strip()
        cusa = self.cusa_var.get().strip().upper()
        
        if not all([ip, port, cusa]):
            messagebox.showwarning("Incomplete Data", "Console IP, Port, and CUSA ID are mandatory.")
            return
            
        if not self.current_image_path:
            messagebox.showwarning("Missing Asset", "Please load an image before pushing.")
            return
            
        self.status_var.set("Compiling image payload...")
        self.root.update()
        
        try:
            img = Image.open(self.current_image_path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            img_byte_arr = BytesIO()
            img.save(img_byte_arr, format='PNG')
            
            self.status_var.set(f"Establishing FTP stream to {ip}:{port}...")
            self.root.update()
            
            ftp = FTP()
            ftp.connect(ip, int(port), timeout=15)
            ftp.login()
            
            target_dir = f"/user/appmeta/{cusa}"
            try:
                ftp.cwd(target_dir)
            except Exception:
                messagebox.showerror("Directory Error", f"Cannot resolve {target_dir}.\nEnsure the CUSA ID is correct and the game is installed.")
                ftp.quit()
                self.status_var.set("Operation halted.")
                return
            
            for filename in filenames:
                self.status_var.set(f"Injecting {filename}...")
                self.root.update()
                img_byte_arr.seek(0)
                ftp.storbinary(f"STOR {filename}", img_byte_arr)
                
            ftp.quit()
            self.status_var.set("Payload delivered successfully.")
            messagebox.showinfo("Success", f"Modifications applied to {cusa}.")
            
        except Exception as e:
            self.status_var.set("Network or transfer failure.")
            messagebox.showerror("Execution Error", str(e))

    def process_external(self):
        self.upload_via_ftp((512, 512), ["icon0.png"])

    def process_internal(self):
        self.upload_via_ftp((1920, 1080), ["pic0.png", "pic1.png"])

if __name__ == "__main__":
    root = tk.Tk()
    app = PS4AppMetaManager(root)
    root.mainloop()
