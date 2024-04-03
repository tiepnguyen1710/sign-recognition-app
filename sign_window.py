import tkinter as tk
from tkinter import Frame, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
import cv2
from PIL import Image, ImageTk
from pathlib import Path
import requests
  

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

        x = (screen_width - 1200) // 2
        y = (screen_height - 800) // 2

        self.master.geometry(f"1200x700+{x}+{y}")

        self.main_frame = Frame(self.master, width=700, height=500, bg="white")
        self.main_frame.place(relx=0.5, rely=0.42, anchor=tk.CENTER)
        self.main_frame.pack_propagate(False)  

        self.label = Label(self.main_frame)
        self.label.pack()

        self.cap = cv2.VideoCapture(0)
        

        self.text_label = Label(self.master, text="hello", font=("Arial", 17))
        self.text_label.place(relx=0.5, rely=0.83, anchor=tk.CENTER)

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
        self.data_from_server()
    
    #def detect_sign(self):
        #self.text_label.config(text="Hello World!")

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
    
    def data_from_server(self):
        response = requests.post('http://localhost:5000/api/data')
        if response.status_code == 200:
            data = response.json()
            self.display_received_data(data)
        else:
            print("Error fetching data")
            self.master.after(1000, self.data_from_server)
    
    def display_received_data(self, data):
        received_data = data.get('data')
        if received_data:
            self.text_label.config(text=received_data)
        else:
            print("No data received")
        self.master.after(1000, self.data_from_server)

if __name__ == "__main__":
    root = tk.Tk()
    sign_window = SignWindow(root)
    sign_window.detect_sign()
    root.mainloop()
