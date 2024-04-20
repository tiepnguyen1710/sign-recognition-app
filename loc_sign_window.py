# import tkinter as tk
# from tkinter import Frame, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, Label
# import cv2
# from PIL import Image, ImageTk
# from pathlib import Path
# import requests
# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / Path(r"assets\frame0")


# class SignWindow:

#     @staticmethod
#     def relative_to_assets(path: str) -> Path:
#         return ASSETS_PATH / Path(path)
    
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Sign Recognition")
#         screen_width = self.master.winfo_screenwidth()
#         screen_height = self.master.winfo_screenheight()

#         x = (screen_width - 1200) // 2
#         y = (screen_height - 800) // 2

#         self.master.geometry(f"1200x700+{x}+{y}")

#         self.main_frame = Frame(self.master, width=700, height=480, bg="white")
#         self.main_frame.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
#         self.main_frame.pack_propagate(False)  

#         self.label = Label(self.main_frame)
#         self.label.pack()

#         self.cap = cv2.VideoCapture(0)
        

#         self.text_label = Label(self.master, text="", font=("Arial", 12))
#         self.text_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

#         self.button = Button(
#             self.master, 
#             text="Click", 
#             bg="#4CAF50",  
#             fg="white",    
#             font=("Arial", 12),  
#             relief="raised",     
#             borderwidth=2,       
#             padx=10,             
#             pady=5                
#         )
#         self.button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

#         self.canvas = Canvas(self.master, width=1200, height=150)
#         self.canvas.place(x = 0, y = 0)
        
#         self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))

#         self.canvas.create_image(55.0, 72.0, image=self.image_image_2)

#         self.canvas.create_text(
#             90.0,
#             56.0,
#             anchor="nw",
#             text="SIGN RECOGNITION",
#             fill="#000000",
#             font=("Lato Bold", 27 * -1)
#         )           
        
#         self.show_frame()
    
#     def detect_sign(self):
#         # self.text_label.config(text="Hello World!")
#         ret, frame = self.cap.read()
#         if ret:
#             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             _, img_encoded = cv2.imencode('.jpg', frame)
#             response = requests.post("http://<AI_IP_ADDRESS>/api/process_image", data=img_encoded.tostring())
#             if response.status_code == 200:
#                 print("Image sent successfully!")
#             else:
#                 print("Failed to send image:", response.status_code)
#     def show_frame(self):
#         # ret, frame = self.cap.read()
#         # if ret:
#         #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         #     frame = cv2.resize(frame, (self.main_frame.winfo_width(), self.main_frame.winfo_height()))

#         #     img = Image.fromarray(frame)
#         #     img = ImageTk.PhotoImage(image=img)
#         #     self.label.img = img
#         #     self.label.config(image=img)
#         #     self.label.after(10, self.show_frame)
#         url = 'http://192.168.1.21/cam-hi.jpg'
#         imgResp = requests.get(url)
#         imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8)
#         img = cv2.imdecode(imgNp, -1)
#         frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         frame = cv2.resize(frame, (self.main_frame.winfo_width(), self.main_frame.winfo_height()))

#         img = Image.fromarray(frame)
#         img = ImageTk.PhotoImage(image=img)
#         self.label.img = img
#         self.label.config(image=img)
#         self.label.after(10, self.show_frame)



# if __name__ == "__main__":
#     root = tk.Tk()
#     sign_window = SignWindow(root)
#     root.mainloop()





# import tkinter as tk
# from tkinter import Frame, Tk, Canvas, Button, PhotoImage, Label
# from PIL import Image, ImageTk
# import paho.mqtt.client as mqtt
# import numpy as np
# import cv2
# import requests

# class SignWindow:

#     def __init__(self, master):
#         self.master = master
#         self.master.title("Sign Recognition")
#         screen_width = self.master.winfo_screenwidth()
#         screen_height = self.master.winfo_screenheight()

#         x = (screen_width - 1200) // 2
#         y = (screen_height - 800) // 2

#         self.master.geometry(f"1200x700+{x}+{y}")

#         self.main_frame = Frame(self.master, width=700, height=480, bg="white")
#         self.main_frame.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
#         self.main_frame.pack_propagate(False)  

#         self.label = Label(self.main_frame)
#         self.label.pack()

#         self.text_label = Label(self.master, text="", font=("Arial", 12))
#         self.text_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

#         self.button = Button(
#             self.master, 
#             text="Click", 
#             bg="#4CAF50",  
#             fg="white",    
#             font=("Arial", 12),  
#             relief="raised",     
#             borderwidth=2,       
#             padx=10,             
#             pady=5                
#         )
#         self.button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

#         self.canvas = Canvas(self.master, width=1200, height=150)
#         self.canvas.place(x = 0, y = 0)
        
#         self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))

#         self.canvas.create_image(55.0, 72.0, image=self.image_image_2)

#         self.canvas.create_text(
#             90.0,
#             56.0,
#             anchor="nw",
#             text="SIGN RECOGNITION",
#             fill="#000000",
#             font=("Lato Bold", 27 * -1)
#         )           
        
#         self.show_frame()

#         # MQTT setup
#         self.mqtt_client = mqtt.Client()
#         self.mqtt_client.on_connect = self.on_connect
#         self.mqtt_client.on_message = self.on_message
#         self.mqtt_client.connect("mqtt.example.com", 1883, 60)
#         self.mqtt_client.loop_start()

#     def on_connect(self, client, userdata, flags, rc):
#         print("Connected with result code "+str(rc))
#         self.mqtt_client.subscribe("cam/image")

#     def on_message(self, client, userdata, msg):
#         print("Message received!")
#         img = cv2.imdecode(np.frombuffer(msg.payload, np.uint8), -1)
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         img = cv2.resize(img, (self.main_frame.winfo_width(), self.main_frame.winfo_height()))
#         img = Image.fromarray(img)
#         img = ImageTk.PhotoImage(image=img)
#         self.label.img = img
#         self.label.config(image=img)

#         # Gửi ảnh từ MQTT về phía AI
#         _, img_encoded = cv2.imencode('.jpg', cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))
#         response = requests.post("http://<AI_IP_ADDRESS>/api/process_image", data=img_encoded.tostring())
#         if response.status_code == 200:
#             print("Image sent successfully!")
#         else:
#             print("Failed to send image:", response.status_code)

#     def relative_to_assets(self, path: str) -> str:
#         return f"assets/frame0/{path}"

#     def show_frame(self):
#         self.master.after(1000, self.show_frame)


# if __name__ == "__main__":
#     root = tk.Tk()
#     sign_window = SignWindow(root)
#     root.mainloop()














# import tkinter as tk
# from tkinter import Label
# from PIL import Image, ImageTk
# import requests
# import numpy as np
# import cv2

# class SignWindow:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Sign Recognition")
#         screen_width = self.master.winfo_screenwidth()
#         screen_height = self.master.winfo_screenheight()

#         x = (screen_width - 640) // 2
#         y = (screen_height - 480) // 2

#         self.master.geometry(f"640x480+{x}+{y}")

#         self.label = Label(self.master)
#         self.label.pack()

#         # HTTP endpoint for video streaming
#         self.endpoint = "http://192.168.1.17/cam.mjpeg"

#         # Start video streaming
#         self.show_video()

#     def show_video(self):
#         # Send HTTP request to ESP32-CAM and get the response
#         response = requests.get(self.endpoint, stream=True)

#         # Process the response data as video frames
#         if response.status_code == 200:
#             # Initialize an empty byte array to store the video frames
#             img_array = bytearray()

#             # Loop through the response content and append to the byte array
#             for chunk in response.iter_content(chunk_size=1024):
#                 img_array.extend(chunk)
                
#                 # Search for the end of frame marker
#                 if b'\xff\xd9' in img_array:
#                     # Decode the frame
#                     frame = cv2.imdecode(np.asarray(img_array, dtype=np.uint8), cv2.IMREAD_COLOR)
                    
#                     # Resize the frame to fit the display window
#                     frame = cv2.resize(frame, (640, 480))
                    
#                     # Convert the frame from BGR to RGB format
#                     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
#                     # Convert the frame to PhotoImage format for display
#                     img = Image.fromarray(frame)
#                     img = ImageTk.PhotoImage(image=img)
                    
#                     # Update the label with the new frame
#                     self.label.img = img
#                     self.label.config(image=img)
                    
#                     # Clear the byte array for the next frame
#                     img_array.clear()

#                     # Break the loop to process the next frame
#                     break
                
#             # Schedule the next frame update after 10 milliseconds
#             self.master.after(10, self.show_video)
#         else:
#             print("Failed to receive video stream")

# if __name__ == "__main__":
#     root = tk.Tk()
#     sign_window = SignWindow(root)
#     root.mainloop()










# import tkinter as tk
# from tkinter import Frame, Button, PhotoImage, Toplevel, Label
# import cv2
# import numpy as np
# from PIL import Image, ImageTk
# import requests
# from pathlib import Path

# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

# class SignWindow:
#     @staticmethod
#     def relative_to_assets(path: str) -> Path:
#         return ASSETS_PATH / Path(path)
    
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Sign Recognition")
#         screen_width = self.master.winfo_screenwidth()
#         screen_height = self.master.winfo_screenheight()

#         x = (screen_width - 1200) // 2
#         y = (screen_height - 800) // 2

#         self.master.geometry(f"1200x700+{x}+{y}")

#         self.main_frame = Frame(self.master, width=700, height=480, bg="white")
#         self.main_frame.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
#         self.main_frame.pack_propagate(False)  

#         self.label = Label(self.main_frame)
#         self.label.pack()

#         self.text_label = Label(self.master, text="", font=("Arial", 12))
#         self.text_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

#         self.button = Button(
#             self.master, 
#             text="Click", 
#             bg="#4CAF50",  
#             fg="white",    
#             font=("Arial", 12),  
#             relief="raised",     
#             borderwidth=2,       
#             padx=10,             
#             pady=5,
#             command=self.detect_sign
#         )
#         self.button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

#         self.canvas = tk.Canvas(self.master, width=1200, height=150)
#         self.canvas.place(x=0, y=0)
        
#         self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
#         self.canvas.create_image(55.0, 72.0, image=self.image_image_2)

#         self.canvas.create_text(
#             90.0,
#             56.0,
#             anchor="nw",
#             text="SIGN RECOGNITION",
#             fill="#000000",
#             font=("Lato Bold", 27 * -1)
#         )           
        
#         self.show_frame()
    
#     def detect_sign(self):
#         try:
#             ret, frame = self.cap.read()
#             if ret:
#                 _, img_encoded = cv2.imencode('.jpg', frame)
#                 response = requests.post("http://<AI_IP_ADDRESS>/api/process_image", data=img_encoded.tostring())
#                 if response.status_code == 200:
#                     print("Image sent successfully!")
#                 else:
#                     print("Failed to send image:", response.status_code)
#             pass
#         except Exception as e:
#             print("Error:", e)
#             self.text_label.config(text="Lỗi 1")
    
#     def show_frame(self):
#         try:
#             url = 'http://192.168.1.17/cam.mjpeg'
#             imgResp = requests.get(url)
#             imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8)
#             img = cv2.imdecode(imgNp, -1)
#             frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             frame = cv2.resize(frame, (self.main_frame.winfo_width(), self.main_frame.winfo_height()))
#             img = Image.fromarray(frame)
#             img = ImageTk.PhotoImage(image=img)
#             self.label.img = img
#             self.label.config(image=img)
#             self.label.after(10, self.show_frame)
#         except Exception as e:
#             print("Error:", e)
#             self.text_label.config(text="Lỗi 2")

# if __name__ == "__main__":
#     root = tk.Tk()
#     sign_window = SignWindow(root)
#     root.update_idletasks()  
#     root.deiconify()
#     root.mainloop()












# import tkinter as tk
# from tkinter import Frame, Button, PhotoImage, Toplevel, Label
# import cv2
# import numpy as np
# from PIL import Image, ImageTk
# import requests
# from pathlib import Path
# import sys

# OUTPUT_PATH = Path(__file__).parent
# ASSETS_PATH = OUTPUT_PATH / "assets" / "frame0"

# class SignWindow:
#     @staticmethod
#     def relative_to_assets(path: str) -> Path:
#         return ASSETS_PATH / Path(path)
    
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Sign Recognition")
#         screen_width = self.master.winfo_screenwidth()
#         screen_height = self.master.winfo_screenheight()

#         x = (screen_width - 1200) // 2
#         y = (screen_height - 800) // 2

#         self.master.geometry(f"1200x700+{x}+{y}")

#         self.main_frame = Frame(self.master, width=700, height=480, bg="white")
#         self.main_frame.place(relx=0.5, rely=0.43, anchor=tk.CENTER)
#         self.main_frame.pack_propagate(False)  

#         self.label = Label(self.main_frame)
#         self.label.pack()

#         self.text_label = Label(self.master, text="", font=("Arial", 12))
#         self.text_label.place(relx=0.5, rely=0.86, anchor=tk.CENTER)

#         self.button = Button(
#             self.master, 
#             text="Click", 
#             bg="#4CAF50",  
#             fg="white",    
#             font=("Arial", 12),  
#             relief="raised",     
#             borderwidth=2,       
#             padx=10,             
#             pady=5,
#             command=self.detect_sign
#         )
#         self.button.place(relx=0.5, rely=0.93, anchor=tk.CENTER)

#         self.close_button = Button(
#             self.master, 
#             text="Close", 
#             bg="#FF6347",  
#             fg="white",    
#             font=("Arial", 12),  
#             relief="raised",     
#             borderwidth=2,       
#             padx=10,             
#             pady=5,
#             command=self.close_window
#         )
#         self.close_button.place(relx=0.9, rely=0.93, anchor=tk.CENTER)

#         self.canvas = tk.Canvas(self.master, width=1200, height=150)
#         self.canvas.place(x=0, y=0)
        
#         self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
#         self.canvas.create_image(55.0, 72.0, image=self.image_image_2)

#         self.canvas.create_text(
#             90.0,
#             56.0,
#             anchor="nw",
#             text="SIGN RECOGNITION",
#             fill="#000000",
#             font=("Lato Bold", 27 * -1)
#         )           
        
#         self.show_frame()
    
#     def detect_sign(self):
#         try:
#             ret, frame = self.cap.read()
#             if ret:
#                 _, img_encoded = cv2.imencode('.jpg', frame)
#                 response = requests.post("http://<AI_IP_ADDRESS>/api/process_image", data=img_encoded.tostring())
#                 if response.status_code == 200:
#                     print("Image sent successfully!")
#                 else:
#                     print("Failed to send image:", response.status_code)
#             pass
#         except Exception as e:
#             print("Error:", e)
#             self.text_label.config(text="Lỗi 1")
    
#     def show_frame(self):
#         try:
#             url = 'http://192.168.1.17/cam.mjpeg'
#             imgResp = requests.get(url, timeout=1)  # Sử dụng timeout để giới hạn thời gian kết nối
#             imgNp = np.array(bytearray(imgResp.content), dtype=np.uint8)
#             img = cv2.imdecode(imgNp, -1)
#             frame = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             frame = cv2.resize(frame, (self.main_frame.winfo_width(), self.main_frame.winfo_height()))
#             img = Image.fromarray(frame)
#             img = ImageTk.PhotoImage(image=img)
#             self.label.img = img
#             self.label.config(image=img)
#             self.label.after(10, self.show_frame)
#         except Exception as e:
#             print("Error:", e)
#             self.text_label.config(text="Lỗi 2")
    
#     def close_window(self):
#         self.master.destroy()

# if __name__ == "__main__":
#     root = tk.Tk()
#     sign_window = SignWindow(root)
#     root.update_idletasks()  
#     root.deiconify()
#     root.mainloop()
#     sys.exit()







import cv2
import urllib.request
import numpy as np
from tkinter import Toplevel, Label
from tkinter import Tk
import requests

url = 'http://192.168.1.12/cam.mjpeg'  
def get_stream():
    try:
        stream = urllib.request.urlopen(url)
        bytes = b''
        while True:
            bytes += stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b+2]
                bytes = bytes[b+2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                yield frame
    except Exception as e:
        print("Error:", e)
        yield None
def process_stream():
    for frame in get_stream():
        if frame is not None:
            send_frame_to_ai(frame)
        else:
            print("Lỗi khi nhận frame từ camera")
def send_frame_to_ai(frame):
    try:
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post('http://127.0.0.1:5000/predict', files={'image': img_encoded.tostring()})
        if response.status_code == 200:
            print(response.content)
            print("Frame đã được gửi thành công cho AI!")
        else:
            print("Lỗi khi gửi frame cho AI:", response.status_code)
    except Exception as e:
        print("Lỗi khi gửi frame cho AI:", e)
def display_stream():
    cv2.namedWindow('ESP32-CAM Stream', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('ESP32-CAM Stream', 640, 480)  # Thay đổi kích thước cửa sổ hiển thị

    cv2.imshow('ESP32-CAM Stream', np.zeros((480, 640, 3), dtype=np.uint8))  # Hiển thị cửa sổ trước khi kết nối

    for frame in get_stream():
        if frame is not None:
            cv2.imshow('ESP32-CAM Stream', frame)
            send_frame_to_ai(frame)
        else:
            print("Lỗi cam")  # In lỗi ra cửa sổ console
        if cv2.waitKey(1) == 27:  # Nhấn phím Esc để thoát
            break

    cv2.destroyAllWindows()
def show_window():
    window = Tk()
    window.title("Sign Window")
    display_stream()
    cv2.destroyAllWindows()
    window.mainloop()
if __name__ == "__main__":
    display_stream()
    cv2.destroyAllWindows()




