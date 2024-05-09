
import cv2
import numpy as np
import base64
from tkinter import Label, Button, Text, font as tkfont
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import threading
import requests

subnet = '192.168.1'  
username = "admin"
password = "admin123"

class CameraApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera App")
        self.cap = None
        self.frame = None
        self.running = False
        self.master.title("Camera App")
        self.master.geometry("1024x800")  # Đặt kích thước cửa sổ
        self.master.configure(bg="#f0f0f0") 
        self.consecutive_count = 0  
        self.last_predicted_char = None
        # # Thiết lập các khung
        # self.video_frame = tk.Frame(self.master)
        # self.video_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # self.control_frame = tk.Frame(self.master)
        # self.control_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0, 20))

        # self.text_field_frame = tk.Frame(self.master)
        # self.text_field_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0, 20))

        self.esp_running = False
        self.create_widgets()

    def create_widgets(self):
        # Khung chứa phần hiển thị video
        self.video_frame = tk.Frame(self.master, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Label hiển thị video
        self.video_panel = Label(self.video_frame, bg="black")
        self.video_panel.pack(fill=tk.BOTH, expand=True)

        # Khung chứa các nút điều khiển và trạng thái
        self.control_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.control_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0, 20))

        # Nút Start Camera
        self.start_button = Button(self.control_frame, text="Start Camera", command=self.start_camera, width=15, bg="#4CAF50", fg="white", font=("Arial", 20, "bold"))
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        # Nút Stop Camera
        self.stop_button = Button(self.control_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED, width=15, bg="#f44336", fg="white", font=("Arial", 20, "bold"))
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        # Nút Find Camera
        self.find_camera_button = Button(self.control_frame, text="Find Camera", command=self.find_camera, width=15, bg="#2196F3", fg="white", font=("Arial", 20, "bold"))
        self.find_camera_button.grid(row=0, column=2, padx=5, pady=5)

        # Label trạng thái
        self.status_label = Label(self.control_frame, text="", fg="blue", bg="#f0f0f0", font=("Arial", 20))
        self.status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=5)

        # Khung chứa vùng hiển thị kết quả
        self.text_field_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.text_field_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0, 20))

        # Vùng hiển thị kết quả
        self.text_field = Text(self.text_field_frame, font=("Arial", 40))
        self.text_field.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text_field.insert(tk.END, "HI")

    # def __init__(self, master):
    #     self.master = master
    #     self.master.title("Camera App")
    #     self.cap = None
    #     self.frame = None
    #     self.window_width = 1024
    #     self.window_height = 800
    #     self.running = False
    #     self.video_frame = tk.Frame(self.master, width=self.window_width - 50, height=self.window_height - 200)
    #     self.video_frame.pack()
    #     self.esp_running = False
    #     self.control_frame = tk.Frame(self.master)
    #     self.control_frame.pack()

    #     self.text_field_frame = tk.Frame(self.master, width=self.window_width, height=200)
    #     self.text_field_frame.pack()
    #     self.consecutive_count = 0  
    #     self.last_predicted_char = None
    #     self.text_font = tkfont.Font(family="Arial", size=50)
    #     self.create_widgets()

    # def create_widgets(self):
    #     self.video_panel = Label(self.video_frame)
    #     self.video_panel.pack(fill=tk.BOTH, expand=True)

    #     self.start_button = Button(self.control_frame, text="Start Camera",command=self.start_camera)
    #     self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

    #     self.stop_button = Button(self.control_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
    #     self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

    #     self.find_camera_button = Button(self.control_frame, text="Find Camera", command=self.find_camera)
    #     self.find_camera_button.pack(side=tk.LEFT, padx=10, pady=5)

    #     self.status_label = Label(self.control_frame, text="", fg="blue")
    #     self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

    #     self.text_field = tk.Text(self.master, font=self.text_font)
    #     self.text_field.pack()

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.find_camera_button.config(state=tk.DISABLED)
            self.status_label.config(text="Camera started")
            self.show_frame()

    def stop_camera(self):
        if self.running:
            self.running = False 
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.find_camera_button.config(state=tk.NORMAL)
            self.status_label.config(text="Camera stopped")
            if self.frame is not None:
                self.frame = None
                self.video_panel.config(image="")

    def find_camera(self):
        self.status_label.config(text="Searching camera...")
        result_cam_ip = self.find_esp32_cam()
        if result_cam_ip:
            print('ESP32-CAM found at IP address:', result_cam_ip)
            self.status_label.config(text=f"ESP32-CAM found at IP address: {result_cam_ip}")
            self.get_stream(result_cam_ip, self.text_field)
        else:
            print("Timeout occurred while searching for camera")
            self.status_label.config(text="Timeout occurred while searching for camera")
            self.find_camera_button.config(state=tk.NORMAL)  
            self.start_button.config(state=tk.NORMAL) 
            self.stop_button.config(state=tk.DISABLED)
    def find_esp32_cam(self):
        cam_ip = None
        found_event = threading.Event()
        semaphore = threading.Semaphore(10)  
        threads_count = 0
        def check_ip(ip):
            nonlocal cam_ip,threads_count
            # print('ip: ', ip, '\n')
            try:
                response = requests.get(f'http://{ip}/cam_status', auth=(username, password), timeout=10)
                print(f"Response from IP {ip}: {response.status_code} \n")
                if response.status_code == 200 and response.text.strip() == "ESP32-CAM":
                    with semaphore:  
                        cam_ip = ip
                        found_event.set()  
            except requests.exceptions.RequestException as e:
                pass
            finally:
                threads_count += 1
                if threads_count == 255:
                    found_event.set()
        
        threads = []
        for i in range(1, 256):
            thread = threading.Thread(target=check_ip, args=(f'{subnet}.{i}',))
            threads.append(thread)
            thread.start()
        
        found_event.wait(timeout=3)  
        
        for thread in threads:
            thread.join(timeout=0.1)  
        
        return cam_ip
    
    
    def send_frame_to_ai(self, frame,text_field):
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post('http://127.0.0.1:5000/predict', files={'image': img_encoded.tostring()})
        
        if response.status_code == 200: 
            prediction = response.json()
            predicted_char = prediction.get('predicted_char', '')
            print("Nhận kí tự từ AI:", predicted_char)
            if predicted_char == self.last_predicted_char:
                self.consecutive_predictions.append(predicted_char)
            else:
                self.consecutive_predictions = [predicted_char]
                self.last_predicted_char = predicted_char

            if len(self.consecutive_predictions) == 5:
                if predicted_char == "nothing":
                    pass
                elif predicted_char == "space":
                    text_field.insert(tk.END, " ")
                elif predicted_char == "del":
                    current_text = text_field.get("1.0", tk.END)
                    if len(current_text) > 1:
                        text_field.delete("end-2c")
                else:
                    text_field.insert(tk.END, predicted_char)
                    
                self.consecutive_predictions = []  
        
    def get_stream(self, cam_ip, text_field):
        self.esp_running = True
        print('cam_ip: ', cam_ip)
        print('get stream')
        if cam_ip is None:
            print("No ESP32-CAM found in the network")
            return
        url = f'http://{cam_ip}/cam.mjpeg'
        auth_header = 'Basic ' + base64.b64encode(f'{username}:{password}'.encode()).decode()
        request = urllib.request.Request(url)
        request.add_header('Authorization', auth_header)
        stream = urllib.request.urlopen(request)
        bytes = b''
        while self.esp_running:
            bytes += stream.read(1024)
            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')
            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]
                frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                x1, y1, x2, y2 = 100, 100, 300, 300
                self.send_frame_to_ai(frame,text_field)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.imshow('ESP32-CAM Stream', frame)
                if cv2.waitKey(1) == 27:
                    self.esp_running = False
                    self.stop_camera()
                    self.status_label.config(text="Exit Esp32 CAM")
                    break

    def show_frame(self):
        _, frame = self.cap.read()
        if frame is not None:
            # Vẽ hình vuông focus
            x1, y1, x2, y2 = 50, 50, 200, 200
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = Image.fromarray(self.frame)
            self.frame = ImageTk.PhotoImage(self.frame)
            self.video_panel.config(image=self.frame)
            self.video_panel.image = self.frame
            # self.send_frame_to_ai(frame,self.text_field)
            self.video_panel.after(10, self.show_frame)  
        else:
            self.stop_camera()
            self.status_label.config(text="Error: Failed to capture frame")

def main():
    root = tk.Tk()
    CameraApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()

