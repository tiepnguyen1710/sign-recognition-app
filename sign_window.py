import tkinter as tk
from tkinter import Frame, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
import cv2
from PIL import Image, ImageTk
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


class SignWindow:

    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)
    
    def __init__(self, master):
        self.master = master
        self.master.title("Sign Recognition")
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Tính toán vị trí để đặt cửa sổ vào giữa màn hình
        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2

        self.master.geometry(f"1200x700+{x}+{y}")

        self.main_frame = Frame(self.master, width=700, height=480, bg="white")
        self.main_frame.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
        self.main_frame.pack_propagate(False)  

        self.label = Label(self.main_frame)
        self.label.pack()

        self.cap = cv2.VideoCapture(0)
        

        self.text_label = Label(self.master, text="", font=("Arial", 12))
        self.text_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

        self.button = Button(
            self.master, 
            text="Click", 
            bg="#4CAF50",  
            fg="white",    
            font=("Arial", 12),  
            relief="raised",     
            borderwidth=2,       
            padx=10,             
            pady=5                
        )
        self.button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

        self.canvas = Canvas(self.master, width=1200, height=150)
        self.canvas.place(x = 0, y = 0)
        
        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))

        self.canvas.create_image(55.0, 72.0, image=self.image_image_2)

        self.canvas.create_text(
            90.0,
            56.0,
            anchor="nw",
            text="SIGN RECOGNITION",
            fill="#000000",
            font=("Lato Bold", 27 * -1)
        )           
        
        self.show_frame()
    
    def detect_sign(self):
        self.text_label.config(text="Hello World!")

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = cv2.resize(frame, (self.main_frame.winfo_width(), self.main_frame.winfo_height()))

            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(image=img)
            self.label.img = img
            self.label.config(image=img)
            self.label.after(10, self.show_frame)



if __name__ == "__main__":
    root = tk.Tk()
    sign_window = SignWindow(root)
    root.mainloop()
