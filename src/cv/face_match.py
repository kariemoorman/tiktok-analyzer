import argparse
import os
import sys
import shutil
import face_recognition

class FaceMatch:
    def __init__(self, image_directory): 
        self.image_directory = image_directory
        self.image_files = [f for f in os.listdir(self.image_directory) if 
f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not self.image_files:
            print("No image files found in the directory. Please specify directory that contains images.")
            sys.exit(1)
    
    def face_check(self): 
        for file in self.image_files: 
            image_path = os.path.join(self.image_directory, file)
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            if not face_encodings: 
                no_faces = os.path.join(self.image_directory, "no_faces")
                os.makedirs(no_faces, exist_ok=True)
                shutil.move(image_path, no_faces)
        self.image_files = [f for f in os.listdir(self.image_directory) if 
f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            

    def compare_faces(self):

        self.face_check()
        
        subdirectory_count = 1
        
        while self.image_files: 
            anchor_file = self.image_files.pop(0)
            anchor_path = os.path.join(self.image_directory, anchor_file)
            anchor_image = face_recognition.load_image_file(anchor_path)
            anchor_encoding = face_recognition.face_encodings(anchor_image)[0]
            
            face_dir = os.path.join(self.image_directory, 
f"face_{subdirectory_count}")
            os.makedirs(face_dir, exist_ok=True)
            shutil.move(anchor_path, face_dir)
            
            for next_file in self.image_files[:]: 
                next_path = os.path.join(self.image_directory, next_file)
                next_image = face_recognition.load_image_file(next_path)
                next_encoding = face_recognition.face_encodings(next_image)[0]
                
                results = face_recognition.compare_faces([anchor_encoding], next_encoding)
                if results[0]: 
                    shutil.move(next_path, face_dir)
                    self.image_files.remove(next_file)
            
            subdirectory_count += 1
        
                
def main():
    parser = argparse.ArgumentParser(description='Image classification based on facial features.')
    parser.add_argument("image_directory", type=str, help='Path to directory containing images.')
    args = parser.parse_args()
    
    image_matcher = FaceMatch(args.image_directory)
    image_matcher.compare_faces()
    
if __name__ == '__main__': 
    main()
