# Home_CCTV_Server
# CCTV 
# Created by Yigang Zhou on 2020-01-09.
# Copyright © 2020 Yigang Zhou. All rights reserved.

import cv2
import time
import threading
import datetime
from pathlib import Path

def draw_time_label(frame):
    """
    为frame加入时间label
    :param frame:
    :return:
    """
    text = time.ctime()
    font_face = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.5
    color = (255, 0, 0)
    thickness = 2

    f = cv2.putText(frame, text, (10, 30), font_face, scale, color, thickness, cv2.LINE_AA)
    return f


class CCTV():

    def __init__(self,save_path='/'):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))
        self.current_hour = -1
        self.record_thread = None
        self.save_path = save_path
        print("CCTV初始化...")
        print("摄像头分辨率", self.frame_width, "x", self.frame_height)
        print("储存路径", self.save_path)


    def __del__(self):
        self.cap.release()

    def start_record(self):

        now = datetime.datetime.now()
        date = str(now.year)+'-'+str(now.month)+'-'+str(now.day)
        hour = now.hour


        if hour != self.current_hour:

            path = self.save_path + date + '/'
            file_path = path + str(hour) + '.mp4'
            Path(path).mkdir(parents=True, exist_ok=True)

            if self.record_thread != None:
                self.record_thread.stop()

            self.record_thread = RecordThread(self.cap, file_path)
            self.record_thread.start()
            self.current_hour = hour
        threading.Timer(1, self.start_record).start()

    def stop_record(self):
        self.record_thread.stop()

    def get_frame(self):
        """
        得到帧，用于Web渲染
        :return:
        """
        success, image = self.cap.read()
        #self.cap.set(3, 320)
        #self.cap.set(4, 240)

        if success:
            image = draw_time_label(image)
            # We are using Motion JPEG, but OpenCV defaults to capture raw images,
            # so we must encode it into JPEG in order to correctly display the
            # video stream.
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        else:
            return bytearray()


class RecordThread(threading.Thread):

    def __init__(self, cap, file_path):
        threading.Thread.__init__(self)
        self.file_path = file_path
        self.cap = cap
        self.frame_width = int(self.cap.get(3))
        self.frame_height = int(self.cap.get(4))

        self.stopped = True
        out = None

    def run(self):
        print("CCTV开始录制", self.file_path)
        self.stopped = False
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        frame_rate = 30

        out = cv2.VideoWriter(self.file_path, fourcc, frame_rate, (self.frame_width, self.frame_height))

        while True:
            ret, frame = self.cap.read()
            frame = draw_time_label(frame)
            if ret:
                out.write(frame)

            if self.stopped:
                # out.release()
                print("录制停止\n")
                break

    def stop(self):
        self.stopped = True
        self.join()
