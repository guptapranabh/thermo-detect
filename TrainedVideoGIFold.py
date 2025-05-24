import gradio as gr
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO
import tempfile

# Load the custom-trained YOLOv8 model
model = YOLO("best.pt")

def process_frame(frame, conf_threshold, iou_threshold):
    """Processes a single frame with YOLOv8 model and returns the annotated frame."""
    results = model.predict(
        source=frame,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
        imgsz=640,
    )
    
    # Use the first result (assuming only one result is needed)
    if results:
        r = results[0]
        im_array = r.plot()
        # Convert the RGB image to BGR format for OpenCV compatibility
        return im_array[..., ::-1]
    return frame

def invert_red_blue(frame):
    """Inverts the red and blue channels of the frame."""
    # Split the frame into its B, G, R channels
    b, g, r = cv2.split(frame)
    # Merge channels back together with R and B swapped
    return cv2.merge([r, g, b])

def predict(input_file, conf_threshold, iou_threshold):
    """Handles both image and video inputs for YOLO inference."""
    if isinstance(input_file, bytes):  # Handle file uploads
        np_arr = np.frombuffer(input_file, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if frame is not None:
            result_img = process_frame(frame, conf_threshold, iou_threshold)
            result_img_path = '/tmp/annotated_image.jpg'
            cv2.imwrite(result_img_path, result_img)
            return result_img_path
        
    elif isinstance(input_file, str):  # It's a file path
        if input_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = cv2.imread(input_file)  # Read image in BGR format
            result_img = process_frame(image, conf_threshold, iou_threshold)
            result_img_path = '/tmp/annotated_image.jpg'
            cv2.imwrite(result_img_path, result_img)
            return result_img_path
        
        elif input_file.lower().endswith(('.mp4', '.avi', '.mov')):
            cap = cv2.VideoCapture(input_file)
            frames = []
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                result_frame = process_frame(frame, conf_threshold, iou_threshold)
                result_frame = invert_red_blue(result_frame)
                frames.append(result_frame)
                
            cap.release()

            if frames:
                gif_path = '/tmp/annotated_video.gif'
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

    return None

# Define Gradio interface
iface = gr.Interface(
    fn=predict,
    inputs=[
        gr.File(label="Upload Image or Video"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence Threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU Threshold"),
    ],
    outputs=gr.Image(label="Annotated GIF"),
    title="Ultralytics YOLOv8 Inference",
    description="Upload images or videos for inference using the Ultralytics YOLOv8 model. The annotated video will be displayed as a GIF.",
)

if __name__ == "__main__":
    iface.launch()
