def send_frame_to_ai(frame):
        _, img_encoded = cv2.imencode('.jpg', frame)
        response = requests.post('http://127.0.0.1:5000/predict', files={'image': img_encoded.tostring()})
        if response.status_code == 200:
            print(response.content)
            print("Frame đã được gửi thành công cho AI!")
        else:
            print("Lỗi khi gửi frame cho AI:", response.status_code)
def get_stream(self, cam_ip):
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
                self.send_frame_to_ai(frame)
                if cv2.waitKey(1) == ord('x'):
                    self.esp_running = False
                    self.stop_camera()
                    self.status_label.config(text="Exit Esp32 CAM")
                    break
# void serveJpg()
# {
#   auto frame = esp32cam::capture();
#   if (frame == nullptr) {
#     Serial.println("CAPTURE FAIL");
#     server.send(503, "", "");
#     return;
#   }
#   Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
#                 static_cast<int>(frame->size()));

#   server.setContentLength(frame->size());
#   server.send(200, "image/jpeg");
#   WiFiClient client = server.client();
#   frame->writeTo(client);
# }

# void handleJpgLo()
# {
#   if (!esp32cam::Camera.changeResolution(loRes)) {
#     Serial.println("SET-LO-RES FAIL");
#   }
#   serveJpg();
# }