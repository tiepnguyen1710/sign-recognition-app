# import cv2
# import urllib.request
# import numpy as np
# from tkinter import Tk as tk
# import requests
# import base64
# from concurrent.futures import ThreadPoolExecutor
# import threading
# from PIL import Image, ImageTk

# subnet = '192.168.1'
# admin_username = "admin"
# admin_password = "admin123"
# def find_esp32_cam():
#     cam_ip = None
#     event = threading.Event()
#     all_threads = []

#     def check_ip(ip):
#         nonlocal cam_ip
#         if cam_ip or event.is_set():  
#             return
#         try:
#             response = requests.get(f'http://{ip}/cam_status', auth=(admin_username, admin_password), timeout=5)
#             if response.status_code == 200 and response.text.strip() == "ESP32-CAM":
#                 cam_ip = ip
#                 print(f"ESP32-CAM found at IP address: {ip}")
#                 event.set()  
#         except requests.exceptions.RequestException:
#             pass
#     cv2.namedWindow('ESP32-CAM Stream', cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('ESP32-CAM Stream', 640, 480)  
#     cv2.imshow('ESP32-CAM Stream', np.zeros((480, 640, 3), dtype=np.uint8))  
#     with ThreadPoolExecutor(max_workers=25) as executor:
#         for i in range(1, 256):
#             thread = threading.Thread(target=check_ip, args=(f'{subnet}.{i}',))
#             all_threads.append(thread)
#             thread.start()
#             executor.submit(check_ip, f'{subnet}.{i}')
#     for thread in all_threads:
#         thread.join()
#     return cam_ip
# def get_stream(cam_ip):
#     if cam_ip is None:
#         print("No ESP32-CAM found in the network")
#         return
#     url = f'http://{cam_ip}/cam.mjpeg'
#     auth_header = 'Basic ' + base64.b64encode(f'{admin_username}:{admin_password}'.encode()).decode()
#     try:
#         request = urllib.request.Request(url)
#         request.add_header('Authorization', auth_header)
#         stream = urllib.request.urlopen(request)
#         bytes = b''
#         while True:
#             bytes += stream.read(1024)
#             a = bytes.find(b'\xff\xd8')
#             b = bytes.find(b'\xff\xd9')
#             if a != -1 and b != -1:
#                 jpg = bytes[a:b+2]
#                 bytes = bytes[b+2:]
#                 frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#                 yield frame
#     except Exception as e:
#         print("Error:", e)
#         yield None
# def send_frame_to_ai(frame):
#     try:
#         _, img_encoded = cv2.imencode('.jpg', frame)
#         response = requests.post('http://127.0.0.1:5000/predict', files={'image': img_encoded.tostring()})
#         if response.status_code == 200:
#             print(response.content)
#             print("Frame đã được gửi thành công cho AI!")
#         else:
#             print("Lỗi khi gửi frame cho AI:", response.status_code)
#     except Exception as e:
#         print("Lỗi khi gửi frame cho AI:", e)
# def display_stream(cam_ip):
#     cv2.namedWindow('ESP32-CAM Stream', cv2.WINDOW_NORMAL)
#     cv2.resizeWindow('ESP32-CAM Stream', 640, 480)  # Thay đổi kích thước cửa sổ hiển thị

#     cv2.imshow('ESP32-CAM Stream', np.zeros((480, 640, 3), dtype=np.uint8))  # Hiển thị cửa sổ trước khi kết nối
#     exit_program = False 
#     for frame in get_stream(cam_ip):
#         if frame is not None:
#             cv2.imshow('ESP32-CAM Stream', frame)
#             draw_square(frame)
#             # send_frame_to_ai(frame)
#         else:
#             print("Lỗi cam")  # In lỗi ra cửa sổ console
        
#         if 0xFF == ord('x'):  
#             print('hi')
#             exit_program = True
#             break
#     if exit_program:
#         cv2.destroyAllWindows()
#         exit(0)
    
# def draw_square(frame):
#     x1, y1, x2, y2 = 100, 100, 300, 300
#     cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

# class CameraApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Camera App")

#         self.frame = None
#         self.cap = None

#         self.create_widgets()

#     def create_widgets(self):
#         self.video_panel = tk.Label(self.master)
#         self.video_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

#         self.start_button = tk.Button(self.master, text="Start Camera", command=self.start_camera)
#         self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

#         self.stop_button = tk.Button(self.master, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
#         self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

#         self.find_camera_button = tk.Button(self.master, text="Find Camera", command=self.find_camera)
#         self.find_camera_button.pack(side=tk.LEFT, padx=10, pady=5)

#         self.status_label = tk.Label(self.master, text="", fg="blue")
#         self.status_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

#     def start_camera(self):
#         if self.cap is None:
#             self.cap = cv2.VideoCapture(0)

#         if self.cap.isOpened():
#             self.start_button.config(state=tk.DISABLED)
#             self.stop_button.config(state=tk.NORMAL)
#             self.find_camera_button.config(state=tk.DISABLED)

#             self.status_label.config(text="Camera started")

#             self.show_frame()

#     def stop_camera(self):
#         if self.cap is not None and self.cap.isOpened():
#             self.cap.release()
#             self.cap = None

#             self.start_button.config(state=tk.NORMAL)
#             self.stop_button.config(state=tk.DISABLED)
#             self.find_camera_button.config(state=tk.NORMAL)

#             self.status_label.config(text="Camera stopped")

#             if self.frame is not None:
#                 self.frame = None
#                 self.video_panel.config(image="")

#     def find_camera(self):
#         cam_ip = find_esp32_cam()
#         if cam_ip:
#             display_stream(cam_ip)
#         else:
#             self.status_label.config(text="Camera stopped")
#     def show_frame(self):
#         _, frame = self.cap.read()
#         if frame is not None:
#             self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             self.frame = Image.fromarray(self.frame)
#             self.frame = ImageTk.PhotoImage(self.frame)

#             self.video_panel.config(image=self.frame)
#             self.video_panel.image = self.frame

#             self.video_panel.after(10, self.show_frame)  # Update frame every 10 milliseconds
#         else:
#             self.stop_camera()
#             self.status_label.config(text="Error: Failed to capture frame")

# def main():
#     root = tk()
#     root.geometry("800x600")  
#     CameraApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()


# self.get_frame(stream, bytes)  
        # except Exception as e:
        #     print("Error in get_stream:", e)
        #     yield None
        # self.esp_running = True
        # print('cam_ip: ', cam_ip)
        # print('get stream')
        # if cam_ip is None:
        #     print("No ESP32-CAM found in the network")
        #     return
        # url = f'http://{cam_ip}/cam.mjpeg'
        # auth = (username, password)
        # try:
        #     cv2.namedWindow('ESP32-CAM Stream', cv2.WINDOW_NORMAL)
        #     cv2.resizeWindow('ESP32-CAM Stream', 640, 480)  # Thay đổi kích thước cửa sổ hiển thị

        #     cv2.imshow('ESP32-CAM Stream', np.zeros((480, 640, 3), dtype=np.uint8))  # Hiển thị cửa sổ trước khi kết nối
        #     response = requests.get(url, auth=auth, stream=True)
        #     response.raise_for_status()  # Kiểm tra nếu có lỗi trong quá trình nhận dữ liệu

        #     bytes = b''
        #     for chunk in response.iter_content(chunk_size=1024):
        #         bytes += chunk
        #         a = bytes.find(b'\xff\xd8')
        #         b = bytes.find(b'\xff\xd9')
        #         if a != -1 and b != -1:
        #             jpg = bytes[a:b + 2]
        #             bytes = bytes[b + 2:]
        #             frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        #             # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #             # frame_pil = Image.fromarray(frame_rgb)
        #             # frame_tk = ImageTk.PhotoImage(frame_pil)
        #             # self.video_panel.config(image=frame_tk)
        #             # self.video_panel.image = frame_tk
        #             cv2.imshow('ESP32-CAM Stream', frame)
        #         if cv2.waitKey(1) == ord('x'):
        #             self.esp_running = False
        #             self.stop_camera()
        #             self.status_label.config(text="Exit Esp32 CAM")
        #             break
        # except requests.exceptions.RequestException as e:
        #     print("Error in get_stream:", e)



# def display_stream(self, cam_ip):
        # self.running = True
        # self.get_stream(cam_ip)
        # for frame in self.get_stream(cam_ip):
        #     cnt = cnt + 1
        #     if not self.running:  
        #         break
        #     if frame is not None:
        #         frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #         frame_pil = Image.fromarray(frame_rgb)
        #         frame_tk = ImageTk.PhotoImage(frame_pil)
        #         print('vẽ frame: ', cnt, "\n")
        #         self.video_panel.config(image=frame_tk)
        #         self.video_panel.image = frame_tk
        #         # self.draw_square(frame)
        #     else:
        #         self.stop_camera()
        #         self.status_label.config(text="Error: Failed to view video")
        #         break
        #     if cv2.waitKey(1) == ord('x'):
        #         self.status_label.config(text="Exit Esp32 CAM")
        #         break


# def get_frame(self, stream, bytes):
#         bytes += stream.read(1024)
#         a = bytes.find(b'\xff\xd8')
#         b = bytes.find(b'\xff\xd9')
#         if a != -1 and b != -1:
#             jpg = bytes[a:b + 2]
#             bytes = bytes[b + 2:]
#             frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             frame_pil = Image.fromarray(frame_rgb)
#             frame_tk = ImageTk.PhotoImage(frame_pil)
#             self.video_panel.config(image=frame_tk)
#             self.video_panel.image = frame_tk
#             self.video_panel.after(10, self.get_frame)
#             # cv2.imshow('ESP32-CAM Stream', frame)
#         if cv2.waitKey(1) == ord('x'):
#             self.esp_running = False
#             self.stop_camera()
#             self.status_label.config(text="Exit Esp32 CAM")






import cv2
import numpy as np
import base64
from tkinter import Label, Button, Text
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
        self.window_width = 1024
        self.window_height = 800
        self.running = False
        self.video_frame = tk.Frame(self.master, width=self.window_width - 50, height=self.window_height - 200)
        self.video_frame.pack()
        self.esp_running = False
        # Tạo khung chứa các button và label
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack()

        self.text_field_frame = tk.Frame(self.master, width=self.window_width, height=200)
        self.text_field_frame.pack()

        self.create_widgets()

    def create_widgets(self):
        self.video_panel = Label(self.video_frame)
        self.video_panel.pack(fill=tk.BOTH, expand=True)

        self.start_button = Button(self.control_frame, text="Start Camera",command=self.start_camera)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.stop_button = Button(self.control_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.find_camera_button = Button(self.control_frame, text="Find Camera", command=self.find_camera)
        self.find_camera_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.status_label = Label(self.control_frame, text="", fg="blue")
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)

        self.text_field = Text(self.text_field_frame)
        self.text_field.pack(fill=tk.BOTH, expand=True)

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
            # print(response.content)
            prediction = response.json()
            predicted_char = prediction.get('predicted_char', '')
            # Xử lý các trường hợp đặc biệt
            if predicted_char == "nothing":
                # Không làm gì nếu không có ký tự được nhận diện
                pass
            elif predicted_char == "space":
                # Thêm dấu cách vào text field
                text_field.insert(tk.END, " ")
            elif predicted_char == "del":
                # Xóa 1 ký tự trước đó nếu có
                current_text = text_field.get("1.0", tk.END)
                if len(current_text) > 1:
                    text_field.delete("end-2c")
            else:
                # Nếu không có trường hợp đặc biệt, thêm ký tự nhận diện vào text field
                text_field.insert(tk.END, predicted_char)
                print("Frame đã được gửi thành công cho AI!: ",predicted_char)
        else:
            print("Lỗi khi gửi frame cho AI:", response.status_code)
        
    def get_stream(self, cam_ip, text_field):
        self.esp_running = True
        print('cam_ip: ', cam_ip)
        print('get stream')
        if cam_ip is None:
            print("No ESP32-CAM found in the network")
            return
        url = f'http://{cam_ip}/cam.mjpeg'
        cv2.namedWindow('ESP32-CAM Stream', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('ESP32-CAM Stream', 640, 480)  # Thay đổi kích thước cửa sổ hiển thị
        cv2.imshow('ESP32-CAM Stream', np.zeros((480, 640, 3), dtype=np.uint8)) 
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
                # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # frame_pil = Image.fromarray(frame_rgb)
                # frame_tk = ImageTk.PhotoImage(frame_pil)
                # self.video_panel.config(image=frame_tk)
                # self.video_panel.image = frame_tk
                cv2.imshow('ESP32-CAM Stream', frame)
                self.send_frame_to_ai(frame,text_field)
                if cv2.waitKey(1) == ord('x'):
                    self.esp_running = False
                    self.stop_camera()
                    self.status_label.config(text="Exit Esp32 CAM")
                    break

    def show_frame(self):
        _, frame = self.cap.read()
        if frame is not None:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.frame = Image.fromarray(self.frame)
            self.frame = ImageTk.PhotoImage(self.frame)
            self.video_panel.config(image=self.frame)
            self.video_panel.image = self.frame
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

