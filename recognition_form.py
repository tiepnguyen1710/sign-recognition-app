
import cv2
import numpy as np
import base64
from tkinter import Label, Button, Text, font as tkfont, Canvas, PhotoImage
import tkinter as tk
from PIL import Image, ImageTk
import urllib.request
import threading
import requests
from pathlib import Path
import subprocess
import argparse
import time
import queue

subnet = '192.168.43'  
username = "admin"
password = "admin123"

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"E:\Learn DUT\Year 3\PBL5\Interface\sign-recognition-app\assets\frame1")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

count_for_send = 0

class CameraApp:
    def __init__(self, master, image, option=1):
        self.subnet = '192.168.34'  
        self.username = "admin"
        self.password = "admin123"
        self.master = master
        self.master.title("Camera App")
        self.cap = None
        self.frame = None
        self.running = False
        self.master.title("Camera App")
        self.consecutive_count = 0  
        self.last_predicted_char = None
        self.max_length = 20
        self.frame_queue = queue.Queue()

        self.esp_running = False

        self.master.geometry("800x600")
        self.master.configure(bg = "#FFFFFF")
        
        self.init_component(image)
        
        self.video_label = tk.Label(self.master)
        self.video_label.place(x=0, y=0, width=800, height=490)
        
        if int(option) == 1:
            self.find_camera()
        else:
            self.start_camera()
        
        self.update_frame()

    def close_form(self):
        subprocess.Popen(["python", "main_form.py"])
        self.master.destroy()
        
    def init_component(self, image1):
        
        self.canvas = Canvas(
            self.master,
            bg = "#FFFFFF",
            height = 600,
            width = 800,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            0.0,
            800.0,
            490.0,
            fill="#D9D9D9",
            outline="")
        self.button_1 = Button(
            image=image1,
            borderwidth=0,
            highlightthickness=0,
            command=self.close_form,
            relief="flat"
        )
        self.button_1.place(
            x=308.0,
            y=536.0,
            width=183.0,
            height=44.0
        )

        self.text = self.canvas.create_text(
            169.0,
            490.0,
            anchor="nw",
            text="",
            fill="#000000",
            font=("Inter", 40 * -1)
        )

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

        # Tăng kích thước và thay đổi font chữ của các nút
        button_font = ("Arial", 20, "bold")

        # Nút Start Camera
        self.start_button = Button(self.control_frame, text="Start Camera", command=self.start_camera, width=15, bg="#4CAF50", fg="white", font=button_font)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        # Nút Stop Camera
        self.stop_button = Button(self.control_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED, width=15, bg="#f44336", fg="white", font=button_font)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        # Nút Find Camera
        self.find_camera_button = Button(self.control_frame, text="Find Camera", command=self.find_camera, width=15, bg="#2196F3", fg="white", font=button_font)
        self.find_camera_button.grid(row=0, column=2, padx=10, pady=10)

        # Label trạng thái
        self.status_label = Label(self.control_frame, text="", fg="blue", bg="#f0f0f0", font=("Arial", 20))
        self.status_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Khung chứa vùng hiển thị kết quả
        self.text_field_frame = tk.Frame(self.master, bg="#f0f0f0")
        self.text_field_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=(0, 20))

        # Vùng hiển thị kết quả
        self.text_field = Text(self.text_field_frame, font=("Arial", 40))
        self.text_field.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.text_field.insert(tk.END, "HI")

    def update_frame(self):
        try:
            if not self.frame_queue.empty():
                imgtk = self.frame_queue.get()
                self.video_label.imgtk = imgtk
                self.video_label.config(image=imgtk)
        except queue.Empty:
            pass
        self.master.after(10, self.update_frame)

    def start_camera(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
        if self.cap.isOpened():
            self.show_frame()

    def stop_camera(self):
        if self.running:
            self.running = False 
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            self.cap = None
            if self.frame is not None:
                self.frame = None
                self.video_panel.config(image="")

    def find_camera(self):
        result_cam_ip = self.find_esp32_cam()
        if result_cam_ip:
            print('ESP32-CAM found at IP address:', result_cam_ip)
            self.get_stream(result_cam_ip, self.text)
        else:
            print("Timeout occurred while searching for camera")

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
        text_value = self.canvas.itemcget(self.text, "text")
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post('http://127.0.0.1:5000/predict', files={'image': img_encoded.tostring()})
        
        if response.status_code == 200: 
            prediction = response.json()
            predicted_char = prediction.get('predicted_char', '')
            print("Nhận kí tự từ AI:", predicted_char, self.consecutive_count)
            if self.last_predicted_char == None or self.last_predicted_char != predicted_char:
                self.last_predicted_char = predicted_char
                self.consecutive_count = 0
            else:
                self.consecutive_count += 1
            if self.consecutive_count == 4:
                self.consecutive_count = 0
                if len(text_value) == self.max_length:
                    text_value = ""
                    self.canvas.itemconfig(self.text, text=text_value)
                elif predicted_char == "nothing":
                    pass
                elif predicted_char == "space":
                    text_value += " "
                    self.canvas.itemconfig(self.text, text=text_value)
                elif predicted_char == "del":
                    if text_value != None or text_value != "":
                        text_value = text_value[-1]
                        self.canvas.itemconfig(self.text, text=text_value)
                else:
                    text_value += predicted_char
                    self.canvas.itemconfig(self.text, text=text_value)
                    
    def get_stream(self, cam_ip, text_field):
        def run_stream():
            global count_for_send
            self.esp_running = True
            print('cam_ip: ', cam_ip)
            print('get stream')
            if cam_ip is None:
                print("No ESP32-CAM found in the network")
                return
            url = f'http://{cam_ip}/cam.mjpeg'
            auth_header = 'Basic ' + base64.b64encode(f'{self.username}:{self.password}'.encode()).decode()
            request = urllib.request.Request(url)
            request.add_header('Authorization', auth_header)
            stream = urllib.request.urlopen(request)
            bytes = b''
            while self.esp_running:
                bytes += stream.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                print("a = ", a, end="\n")
                print("b = ", b, end="\n")
                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    x1, y1, x2, y2 = 90, 90, 310, 310
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    img = Image.fromarray(frame_rgb)
                    imgtk = ImageTk.PhotoImage(image=img)
                    
                    self.frame_queue.put(imgtk)
                    
                    if count_for_send == 10:         
                        cropped_frame = frame[100:300, 100:300]
                        self.send_frame_to_ai(cropped_frame,self.text)
                        count_for_send = 0
                    else:
                        count_for_send +=1

        threading.Thread(target=run_stream).start()

    def show_frame(self):
        global count_for_send
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                x1, y1, x2, y2 = 390, 90, 610, 310
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.flip(frame, 1)
                # Chuyển đổi khung hình từ BGR sang RGB
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Thêm khung hình vào hàng đợi
                self.frame_queue.put(imgtk)
                
                if count_for_send == 10:         
                    # Cắt ảnh trong ô vuông
                    frame2 = cv2.flip(frame, 1)
                    cropped_frame = frame2[100:300, 400:600]
                    cropped_frame2 = cv2.flip(cropped_frame, 1)
                    # Gọi hàm để xử lý ảnh
                    self.send_frame_to_ai(cropped_frame2,self.text)
                    count_for_send = 0
                else:
                    count_for_send +=1
                
                # Gọi show_frame lại sau 10 ms
                self.video_label.after(10, self.show_frame)
            else:
                print("Failed to grab frame")
        else:
            print("Camera is not open")

def main(opt):
    if opt == None:
        opt = 1
    root = tk.Tk()
    a = PhotoImage(
            file=relative_to_assets("button_1.png"))
    CameraApp(root, a, opt)
    root.mainloop()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nhận tham số opt")
    parser.add_argument('--opt', type=int, required=True, help="Tham số opt (ví dụ: --opt 1)")
    args = parser.parse_args()
    main(args.opt)

