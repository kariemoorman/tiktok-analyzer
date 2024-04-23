#!/usr/bin/python3

import cv2
import os
import uuid
import argparse

## Download haarcascade_frontalface_default.xml using the following link, and place it in the : 
#    -  https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_frontalface_default.xml

## For side profile (portrait) use the following link: 
#    -  #https://github.com/opencv/opencv/blob/4.x/data/haarcascades/haarcascade_profileface.xml

current_script_path =  os.path.abspath(__name__)
cv2_base_dir = os.path.dirname(current_script_path)
haar_model = os.path.join(cv2_base_dir, 'src/cv/models/haarcascade_frontalface_default.xml')

class FaceDetection:
    def __init__(self, video_filepath, classifier_path=haar_model):
        self.face_cascade = cv2.CascadeClassifier(classifier_path)
        self.video_filepath = video_filepath.strip()
        self.output_directory = f'{os.path.dirname(video_filepath)}/{os.path.splitext(os.path.basename(video_filepath))[0]}_faces'

    def detect_faces(self):
        cap = cv2.VideoCapture(self.video_filepath)

        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        file_name_wo_extension = f'{os.path.dirname(self.video_filepath)}/{os.path.splitext(os.path.basename(self.video_filepath))[0]}'

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(f'{file_name_wo_extension}-cv_output.mp4', fourcc, 20.0, (frame_width, frame_height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30)
            )
            
            os.makedirs(self.output_directory, exist_ok=True)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

                face_image = frame[y:y + h, x:x + w]
                unique_filename = os.path.join(self.output_directory, f"face_{str(uuid.uuid4())}.png")
                cv2.imwrite(unique_filename, face_image)

            out.write(frame)

            #cv2.imshow('Face Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face Detection in Video Stream")
    parser.add_argument("video_filepath", help="Path to the input video file")
    #parser.add_argument("-o", "--output-directory", default='faces', help="Output directory for saving images of detected faces")
    
    args = parser.parse_args()
    
    detector = FaceDetection(args.video_filepath)
    detector.detect_faces()
