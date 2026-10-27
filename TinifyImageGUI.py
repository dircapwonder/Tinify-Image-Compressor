import os, sys
import tkinter as tk
from tkinter import filedialog, messagebox
import tinify


def icon(name):
    #Return the path of a bundled file (works as .py and as PyInstaller .exe)
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

def add_ext(path, extension):
    if not path.lower().endswith(extension.lower()):
        path += extension
    return path    

class ImageGUI:
    def __init__(self, app):
        self.app = app
        self.app.title("Tinify Image Compressor GUI")
        self.app.geometry("560x600")
        try:
            self.app.iconbitmap(icon("favicon.ico"))
        except tk.TclError:
            pass
        self.selected_file_path = ""
        
        #------------------------------1.) BASICS------------------------------
        #---------------API ENTRY---------------
        tk.Label(app, text="Tinify API Key:", font=("Arial", 10, "bold"), bg="ivory3").pack(anchor="w", pady=5, padx=5)
        self.enter_api = tk.Entry(app, show="#", width=40)
        self.enter_api.pack(anchor="w", pady=5, padx=5)
         
        #---------------IMAGE SELECT---------------
        tk.Label(app, text="Choose an Image:", font=("Arial", 10, "bold"), bg="ivory3").pack(anchor="w", pady=15, padx=5)
        self.select_btn = tk.Button(app, text="Select Image", font=("Arial", 10),bg="ivory3", command=self.c_image)
        self.select_btn.pack(anchor="w", pady=15, padx=5)
        
        self.file_label = tk.Label(app, text="No Image Selected",font=("Arial", 10, "bold"),bg="ivory3", fg="gray47", wraplength=400, justify="left")
        self.file_label.pack(anchor="w", padx=5, pady=6)
        
        #---------------CHOICE---------------
        tk.Label(app, text="Choose an Operation:", font=("Arial", 10, "bold"), bg="ivory3").pack(anchor="w", pady=15, padx=5)
        self.op = tk.IntVar(value=1)
        
        #COMPRESS 
        self.choice_cbtn = tk.Radiobutton(app, text="Compress Image",font=("Arial", 10),bg="ivory3", variable=self.op, value=1, command=self.c_option)
        self.choice_cbtn.pack(anchor="w", padx=10)
        
        #RESIZE
        self.choice_rbtn = tk.Radiobutton(app, text="Resize Image",bg="ivory3", variable=self.op, value=2, command=self.c_option)
        self.choice_rbtn.pack(anchor="w", padx=10)
        
        #------------------------------2.) DYNAMIC CHOICE FRAME------------------------------
        #---------------COMPRESS FRAME---------------
        self.compress_f = tk.LabelFrame(app, text="Compress Settings",font=("Arial", 10),bg="ivory3", padx=15, pady=10)
        self.compress_c = tk.StringVar(value="same") #Default Option
        
        #SAME TYPE
        tk.Radiobutton(self.compress_f, text="Keep the Image Type Same and Compress",font=("Arial", 10),bg="ivory3", variable=self.compress_c, value="same").pack(anchor="w")
        #OPTIMIZED
        tk.Radiobutton(self.compress_f, text="Optimized Compress(Different Image Type)",font=("Arial", 10),bg="ivory3",variable=self.compress_c, value="optimized").pack(anchor="w")
        
        #---------------RESIZE FRAME---------------
        self.resize_f = tk.LabelFrame(app, text="Resize Settings",font=("Arial", 10),bg="ivory3", padx=15, pady=10)
        
        tk.Label(self.resize_f, text="Set Width:",font=("Arial", 10),bg="ivory3").grid(row=0, column=0, sticky="e", pady=2)
        self.enter_w = tk.Entry(self.resize_f, width=10)
        self.enter_w.grid(row=0, column=1, padx=5, pady=2)
        
        tk.Label(self.resize_f, text="Set Height:",font=("Arial", 10),bg="ivory3").grid(row=1, column=0, sticky="e", pady=2)
        self.enter_h = tk.Entry(self.resize_f, width=10)
        self.enter_h.grid(row=1, column=1, padx=5, pady=2)
        
        #---------------DEFAULT CHOICE---------------
        self.compress_f.pack(fill="x", padx=15, pady=15)
        
        #---------------PROCESSING BUTTON---------------
        self.p_button = tk.Button(app, text="Start Processing",font=("Arial", 20, "bold"),bg="honeydew4", fg="white", height=2, width=80, command=self.process)
        self.p_button.pack(anchor="w", pady=45, padx=5)
    
    #------------------------------3.) PROCESS------------------------------
    #---------------HIDE OTHER CHOICE---------------
    def c_option(self): 
        if self.op.get() == 1:
            self.resize_f.pack_forget() #HIDE RESIZE
            self.compress_f.pack(fill="x", padx=15, pady=15, before=self.p_button) #SHOW COMPRESS
        else:
            self.compress_f.pack_forget() #HIDE COMPRESS
            self.resize_f.pack(fill="x", padx=15, pady=15, before=self.p_button) #SHOW RESIZE
    
    #---------------CHOOSE IMAGE---------------            
    def c_image(self):
        file_path = filedialog.askopenfilename(
            title="Choose Image",
            filetypes=[("Supported Image Types", "*.jpg *.jpeg *.png *.webp")])
        if file_path:
            self.selected_file_path = file_path
            self.file_label.config(text=os.path.basename(file_path), fg="green")        
    
    #---------------COMPRESS & RESIZE & API CALL---------------
    def process(self):
        api_key = self.enter_api.get().strip()
        if not api_key:
            messagebox.showerror("ERROR", "Please enter your Tinify API Key!")
            return
        if not self.selected_file_path:
            messagebox.showerror("ERROR", "Please choose an image to process!")
            return

        if self.op.get() == 2:
            w = self.enter_w.get().strip()
            h = self.enter_h.get().strip()

            if not w or not h:
                messagebox.showerror("ERROR", "Please enter width and height!")
                return
            try:
                new_w = int(w)
                new_h = int(h)
            except ValueError:
                messagebox.showerror("ERROR", "Width and height must be whole numbers!")
                return

            if new_w <= 0 or new_h <= 0:
                messagebox.showerror("ERROR", "Please enter positive width and height!")
                return
        
        #--------Validate API Key--------
        tinify.key = api_key
        try: 
            tinify.validate()
        except tinify.AccountError:
            messagebox.showerror("API ERROR", "Your API Key is not valid!")
            return
        except tinify.ConnectionError as e:
            messagebox.showerror("Connection ERROR", f"Could not connect to Tinify:\n{e}")
            return
        except tinify.Error as e:
            messagebox.showerror("API ERROR", f"Tinify error:\n{e}")
            return    
        
        folder = os.path.dirname(self.selected_file_path)
        name, ext = os.path.splitext(os.path.basename(self.selected_file_path))

        save_path = filedialog.asksaveasfilename(
            title="Save As",
            initialdir=folder,
            initialfile=name,   
        )
        if not save_path:    
            return
        
        #---------------Processing---------------
        try:
            source = tinify.from_file(self.selected_file_path)
            #COMPRESS
            if self.op.get() == 1:
                #CONVERT AND COMPRESS
                if self.compress_c.get() == "optimized":
                    converted = source.convert(type=["image/webp", "image/png", "image/jpeg"])
                    save_path = add_ext(save_path, "." + converted.result().extension)
                    converted.to_file(save_path)
                #JUST COMPRESS
                else:
                    source.to_file(add_ext(save_path, ext))
            #RESIZE
            elif self.op.get() == 2:
                resized = source.resize(method="fit", width=new_w, height=new_h)
                resized.to_file(add_ext(save_path, ext))
            messagebox.showinfo("Completed", f"Process completed!\nYour remaining limit for this month: {500 - tinify.compression_count}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            
        
if __name__ == "__main__":
    app = tk.Tk()
    app.configure(bg="ivory3")
    window = ImageGUI(app)
    app.mainloop()
