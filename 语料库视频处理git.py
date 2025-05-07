import cv2

def extract_video_frames(video_path, interval=10):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            if frame_count % interval == 0:
                frames.append(frame)
            frame_count += 1
        else:
            break
    cap.release()
    return frames
