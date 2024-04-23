#!/usr/bin/python3

import argparse
import os
import uuid
from collections import defaultdict
import numpy as np
import cv2
from ultralytics import YOLO
from ultralytics.utils.checks import check_imshow
from ultralytics.utils.plotting import Annotator, colors


current_script_path =  os.path.abspath(__name__)
cv2_base_dir = os.path.dirname(current_script_path)
detect_model = os.path.join(cv2_base_dir, 'src/cv/models/yolov8n.pt')

class ObjectDetection:
    def __init__(self, video_filepath, model='detect'):
        self.video_filepath = video_filepath.strip()
        self.output_directory = f'{os.path.dirname(video_filepath)}/{os.path.splitext(os.path.basename(video_filepath))[0]}_objects'
        if model == 'detect':
            self.model = YOLO(detect_model)
        elif model == 'segment': 
            self.model = YOLO('yolov8n-seg.pt')
        elif model == 'pose': 
            self.model = YOLO('yolov8n-pose.pt')
        else: 
            print('Please specify a CV model: detect, segment, pose.')

    def detect_objects(self):

        names = self.model.names
        track_history = defaultdict(lambda: [])

        file_name_wo_extension = f'{os.path.dirname(self.video_filepath)}/{os.path.splitext(os.path.basename(self.video_filepath))[0]}'
        video_path_out = '{}_objects.mp4'.format(file_name_wo_extension)
        
        # Initialize video capture from local MP4 file
        cap = cv2.VideoCapture(self.video_filepath)

        w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        result = cv2.VideoWriter(video_path_out, fourcc, fps, (w, h))

        while cap.isOpened():
            success, frame = cap.read()
            if success:
                results = self.model.track(frame, persist=True, verbose=False, tracker="botsort.yaml")
                boxes = results[0].boxes.xyxy.cpu()

                if results[0].boxes.id is not None:
                    os.makedirs(self.output_directory, exist_ok=True)

                    # Extract prediction results
                    clss = results[0].boxes.cls.cpu().tolist()
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    confs = results[0].boxes.conf.float().cpu().tolist()

                    # Initialize annotator
                    annotator = Annotator(frame, line_width=2)

                    for box, cls, track_id, conf in zip(boxes, clss, track_ids, confs):
                        label_text = f"{names[int(cls)]} ({conf:.3f}%)"
                        annotator.box_label(box, color=colors(int(cls), True), label=label_text)
                        
                        # Write the object image blocks to the output directory
                        object_image_path = os.path.join(self.output_directory, f"object_{track_id}_{names[int(cls)]}_{str(uuid.uuid4())}.png")
                        object_image = frame[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                        cv2.imwrite(object_image_path, object_image)

                        # Store tracking history
                        track = track_history[track_id]
                        track.append((int((box[0] + box[2]) / 2), int((box[1] + box[3]) / 2)))
                        if len(track) > 30:
                            track.pop(0)

                        # Plot tracks
                        points = np.array(track, dtype=np.int32).reshape((-1, 1, 2))
                        cv2.circle(frame, (track[-1]), 7, colors(int(cls), True), -1)
                        cv2.polylines(frame, [points], isClosed=False, color=colors(int(cls), True), thickness=2)
                        

                result.write(frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                break

        result.release()
        cap.release()
        cv2.destroyAllWindows()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Object Detection in Video Stream")
    parser.add_argument("video_filepath", type=str, help="Path to the input video file")
    parser.add_argument("--model", "-m", type=str, default="detect", help="YOLOV8 Model Type (detect, segment, pose)")
    
    args = parser.parse_args()
    
    detector = ObjectDetection(args.video_filepath, args.model)
    detector.detect_objects()