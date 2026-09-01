import os
from datetime import datetime
import cv2
import numpy as np
from modlib.apps import Annotator
from modlib.devices import AiCamera
from modlib.models import COLOR_FORMAT, MODEL_TYPE, Model
from modlib.models.post_processors import pp_od_yolo_ultralytics

class YOLO(Model):
    def __init__(self):
        super().__init__(
            model_file="packerOut.zip",
            model_type=MODEL_TYPE.CONVERTED,
            color_format=COLOR_FORMAT.RGB,
            preserve_aspect_ratio=False,
        )
        self.labels = np.genfromtxt(
            "labels.txt",
            dtype=str,
            delimiter="\n",
            ndmin=1,
        )

    def post_process(self, output_tensors):
        return pp_od_yolo_ultralytics(output_tensors)

# 保存先フォルダを作成
SAVE_DIR = "detections"
os.makedirs(SAVE_DIR, exist_ok=True)

device = AiCamera(frame_rate=10)
model = YOLO()
device.deploy(model)
annotator = Annotator()

with device as stream:
    for frame in stream:
        detections = frame.detections[frame.detections.confidence > 0.55]

        if len(detections) > 0:
            labels = [f"{model.labels[class_id]}: {score:0.2f}" for _, score, cl                                                                             ass_id, _ in detections]
            annotator.annotate_boxes(frame, detections, labels=labels, alpha=0.3                                                                             , corner_radius=10)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filepath = os.path.join(SAVE_DIR, f"{timestamp}.jpg")

            # frame.image はRGB配列なのでBGRに変換してから保存
            cv2.imwrite(filepath, frame.image)#cv2.cvtColor(frame.image, cv2.COL                                                                             OR_RGB2BGR))
            print(f"Saved: {filepath} ({labels})")