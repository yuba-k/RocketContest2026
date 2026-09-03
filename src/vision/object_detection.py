import os
from datetime import datetime
import cv2
import numpy as np
import queue
import math
import threading
import time
from modlib.apps import Annotator
from modlib.devices import AiCamera
from modlib.models import COLOR_FORMAT, MODEL_TYPE, Model
from modlib.models.post_processors import pp_od_yolo_ultralytics

class YOLO(Model):
    def __init__(self):
        super().__init__(
            model_file="/home/pi/packerOut.zip",
            model_type=MODEL_TYPE.CONVERTED,
            color_format=COLOR_FORMAT.RGB,
            preserve_aspect_ratio=False,
        )
        self.labels = np.genfromtxt(
            "/home/pi/labels.txt",
            dtype=str,
            delimiter="\n",
            ndmin=1,
        )

    def post_process(self, output_tensors):
        return pp_od_yolo_ultralytics(output_tensors)

class Detection():
    def __init__(self):
        #物体角度と距離格納Queue
        self.queue = queue.Queue(maxsize=1)
        # 保存先フォルダを作成
        self.SAVE_DIR = "detections"
        os.makedirs(self.SAVE_DIR, exist_ok=True)

        self.device = AiCamera(frame_rate=10)
        self.model = YOLO()
        self.device.deploy(self.model)
        self.annotator = Annotator()

    def detect(self):
        with self.device as stream:
            for frame in stream:
                detections = frame.detections[frame.detections.confidence > 0.55]

                if len(detections) > 0:
                    labels = [f"{self.model.labels[class_id]}: {score:0.2f}" for _, score, class_id, _ in detections]
                    bbox = detections.bbox[0]
                    cx_norm = (bbox[0]+bbox[2])/2
                    angle = math.degrees(math.atan((cx_norm-0.5)*2*math.tan(math.radians(66)/2)))
                    apparent_height_corm = bbox[3]-bbox[1]
                    distance = 0.7/(2*apparent_height_corm*math.tan(math.radians(52.3)/2))
                    try:
                        # 古いデータがあれば捨てる
                        self.queue.get_nowait()
                    except queue.Empty:
                        pass
                    # 最新データを入れる
                    self.queue.put_nowait({"angle":angle,"distance":distance})
                    self.annotator.annotate_boxes(frame, detections, labels=labels, alpha=0.3, corner_radius=10)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filepath = os.path.join(self.SAVE_DIR, f"{timestamp}.jpg")

                    # frame.image はRGB配列なのでBGRに変換してから保存
                    cv2.imwrite(filepath, frame.image)
    def get_angle_distance(self):
        try:
            return self.queue.get(timeout=1)
        except queue.Empty:
            return None


if __name__ == "__main__":
    model = Detection()
    threading.Thread(target=model.detect, daemon=True).start()
    while True:
        print(model.get_angle_distance())
        time.sleep(0.1)
