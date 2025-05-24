import gradio as gr
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO
import tempfile
import os

# Load the custom-trained YOLOv8 model
model = YOLO("best.pt")

def process_image(image, conf_threshold, iou_threshold):
    """Processes an image with YOLOv8 model and returns the annotated image path."""
    print("Processing image...")
    annotated_image = process_frame(image, conf_threshold, iou_threshold)
    result_img_path = tempfile.mktemp(suffix='.jpg')
    cv2.imwrite(result_img_path, annotated_image)
    return result_img_path

def process_video(video_path, conf_threshold, iou_threshold):
    """Processes a video with YOLOv8 model and returns the path to the annotated GIF."""
    print("Processing video...")
    cap = cv2.VideoCapture(video_path)
    frames = []

    if not cap.isOpened():
        print("Error: Video not opened correctly.")
        return None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Annotate each frame
        annotated_frame = process_frame(frame, conf_threshold, iou_threshold)
        if annotated_frame is not None:
            # Apply color inversion to annotated frames
            b, g, r = cv2.split(annotated_frame)
            inverted_frame = cv2.merge([r, g, b])
            frames.append(inverted_frame)
        else:
            print("Warning: Frame annotation failed.")

    cap.release()

    if frames:
        gif_path = tempfile.mktemp(suffix='.gif')
        pil_frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
        pil_frames[0].save(
            gif_path,
            save_all=True,
            append_images=pil_frames[1:],
            optimize=True,
            duration=100,  # Duration per frame in milliseconds
            loop=0  # Loop count, 0 means infinite loop
        )
        return gif_path

    print("Warning: No frames processed for GIF.")
    return None

def process_frame(frame, conf_threshold, iou_threshold):
    """Annotates a single frame with YOLOv8 model."""
    results = model.predict(
        source=frame,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
        imgsz=640,
    )

    if results:
        r = results[0]
        im_array = r.plot()
        # Convert the RGB image to BGR format for OpenCV compatibility
        return im_array[..., ::-1]
    return frame

def predict(input_file, conf_threshold, iou_threshold):
    """Determines whether input is an image or video and processes accordingly."""
    if isinstance(input_file, bytes):  # Handle file uploads
        np_arr = np.frombuffer(input_file, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if image is not None:
            print("Processing image from byte stream.")
            return process_image(image, conf_threshold, iou_threshold)
        else:
            print("Error: Byte stream cannot be decoded into an image.")
            return None

    elif isinstance(input_file, str):  # File path
        file_extension = input_file.lower().split('.')[-1]

        if file_extension in ('png', 'jpg', 'jpeg'):
            return process_image(input_file, conf_threshold, iou_threshold)

        elif file_extension in ('mp4', 'avi', 'mov'):
            return process_video(input_file, conf_threshold, iou_threshold)

    print("Error: Unsupported file type or file not provided.")
    return None

# Define Gradio interface
iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.File(label="Upload Image or Video"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence Threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU Threshold"),
    ],
    outputs=gr.File(label="Annotated Image or GIF"),  # Handles both image and video outputs
    title="Ultralytics YOLOv8 Inference",
    description="Upload images or videos for inference using the Ultralytics YOLOv8 model. The annotated output will be displayed as an image or GIF.",
)

if __name__ == "__main__":
    iface.launch()
