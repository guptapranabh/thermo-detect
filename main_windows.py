import tempfile
import os
import gradio as gr
import numpy as np
import cv2
from PIL import Image
from ultralytics import YOLO

# loading the model
model = YOLO("best.pt")

# defining issues
issue_descriptions = {
    "-HEATING ISSUE- 30percent-stator winding 3-phase short circuit": "30% stator winding, 3-Phase short circuit detected. Inspect the motor for any internal faults or damage. Repair or replace the damaged windings, check for electrical issues and test the motor thoroughly before returning it to service",
    "-HEATING ISSUE- 30percent-stator winding 2-phase short circuit": "30% stator winding, 2-phase short circuit detected. Inspect the motor, repair or replace damaged windings, and verify the insulation resistance. Regular maintenance checks can prevent recurrence.",
    "-HEATING ISSUE- 50 percent-stator winding 2-phase short circuit": "50% stator winding 2-phase short circuit detected. Shut down the motor and inspect the stator windings for damage. Repair or replace the faulty windings. Ensure proper insulation and conduct a thorough test before restarting.",
    "-HEATING ISSUE- 50percent-stator winding 1-phase short circuit": "50% stator winding 1-phase short circuit detected. Examine the stator windings and identify the cause of the short circuit. Repair or replace thefaulty windings and ensure all electrical connections are secure. Conduct a full functionality test post-repair.",
    "-HEATING ISSUE- Cooling-Fan-issue": "Inspect the cooling fan for damage or obstructions. Repair or replace the fan as necessary. Ensure proper cooling system operation to prevent overheating of the motor.",
    "-HEATING ISSUE- Stuck Rotor Fault": "Rotor may be stuck. Check for mechanical blockages or obstructions preventing rotor movement. Clear any blockages, repair any damaged components, and verify that the rotor is free to turn before restarting the motor.",
    "No issue detected": "no issues are detected, perform routine maintenance checks as per the manufacturer's recommendations. Monitor the motor's performance and ensure all systems are functioning normally."
    # can add more as required
}

def process_frame(frame, conf_threshold, iou_threshold):
    # processing a single frame and returning the annotated frame with results
    results = model.predict(
        source=frame,
        conf=conf_threshold,
        iou=iou_threshold,
        show_labels=True,
        show_conf=True,
        imgsz=640,
    )

    # using the first result (assuming only one result is needed)
    if results:
        r = results[0]
        im_array = r.plot()
        # converting the RGB image to BGR format because OpenCV doesn't work otherwise(idk why yet, should probably read docs), will come back to this issue later
        return im_array[..., ::-1], r
    return frame, None

def invert_red_blue(frame):
    # inverting the red and blue channels of the frame
    b, g, r = cv2.split(frame)
    return cv2.merge([r, g, b])

def extract_labels(result):
    # extract labels from the result
    if result:
        labels = result.names
        boxes = result.boxes  

        extracted_labels = set()
        if boxes is not None:
            for box in boxes:
                class_id = int(box.cls)
                label = labels.get(class_id, "Unknown")
                extracted_labels.add(label)
        return extracted_labels
    return set()

def predict_video(input_file, conf_threshold, iou_threshold):
    # handles video inputs for inference and returns the annotated GIF with proper description."""
    last_frame_labels = set()

    if isinstance(input_file, str) and input_file.lower().endswith(('.mp4', '.avi', '.mov')):
        cap = cv2.VideoCapture(input_file)
        frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            result_frame, result = process_frame(frame, conf_threshold, iou_threshold)
            result_frame = invert_red_blue(result_frame)
            frames.append(result_frame)
            if result:
                last_frame_labels = extract_labels(result)  # update to the labels of the last frame

        cap.release()

        if frames:
            gif_path = os.path.join(tempfile.gettempdir(), "annotated_video.gif")
            pil_frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
            pil_frames[0].save(
                gif_path,
                save_all=True,
                append_images=pil_frames[1:],
                optimize=True,
                duration=100,  # duration per frame in milliseconds
                loop=0  # loop count, 0 = infinite
            )

            # generating description based on the last frame labels
            description = "No specific description available."
            for label in last_frame_labels:
                if label in issue_descriptions:
                    description = issue_descriptions[label]
                    break

            return gif_path, description

    return None, "No result available."

# defining gradio interface for video processing
iface_video = gr.Interface(
    fn=predict_video,
    inputs=[
        gr.File(label="Upload Video"),
        gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence Threshold"),
        gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU Threshold"),
    ],
    outputs=[
        gr.Image(label="Results after observation"),
        gr.Textbox(label="Inspection and repair:", lines=5)
    ],
    title="Thermo Detect",
    description="Upload videos for inference to detect issues. The video will be displayed as a GIF along with a description of detected objects and issues.",
)

if __name__ == "__main__":
    iface_video.launch()
