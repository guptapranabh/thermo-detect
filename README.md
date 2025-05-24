# thermo-detect

**A smart thermal imaging system to detect overheating components, identify the root cause, and provide actionable diagnostics.**

---

## Index

- [Overview](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#overview)
- [Features](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#features)
- [What the current project can/cannot do](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#what-the-current-project-cancannot-do)
- [Getting started](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#getting-started)
- [Installation](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#installation-and-running)
- [How to use](https://github.com/guptapranabh/thermo-detect#how-to-use)
- [Important terms to know about](https://github.com/guptapranabh/thermo-detect#important-terms-to-know-about)
- [Acknowledgements](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#acknowledgements)
---
## Overview

**thermo-detect** uses thermal camera input to:
- Detect overheating components in electronic or mechanical systems.
- Analyze thermal data to identify the most likely source of malfunction.
- Display thermal anomalies and highlight the root cause.
- Provide result summaries and further instructions for maintenance or repair.

Ideal for **hardware diagnostics**, **industrial automation**, **robotics**, and **predictive maintenance**.

---

## Features

- AI root cause detection
- Visual output with bounding boxes on overheating parts of the component
- Provides diagnostic report and actionable output

---

## What the current project can/cannot do:


### Can do:

- Accurately detect failures 
- Provide proper insights

### Cannot do:

- Detect other machinery that is currently out of the trained dataset

  This is partially because complex industrial machinery do not generally overlap with each other,
  hence a custom dataset must be used for each individual equipment.
  As the scope of this project increases, these issues will be resolved

- Does not explicitly support MacOS yet, although it should technically work if you are an experienced developer

## Getting Started

### Prerequisites
- Python 3.9+
- OpenCV, NumPy, and other dependencies as listed in `requirements.txt`


### Installation and running

Clone the repository:
```bash
git clone https://github.com/guptapranabh/thermo-detect.git
```

**For Linux:**

Run `run_linux.sh` on your linux terminal or paste the following set of commands in your console inside the thermo-detect directory:

Make the shell file `run_linux.sh` executable by running the command below:
```bash
chmod +x ./run_linux.sh
```

After that, start the program by running the command below:
```bash
./run_linux.sh
```

**For Windows:**

Run `run_windows.bat` on your Windows system by simply double clicking on it.



### After running the respective scripts:

  
This will open a terminal and start downloading all the neccessary dependencies and start a server, typically on port `http://127.0.0.1:7860/`

Copy and paste the link on your web browser and it should open a WebUI where you can interact with the program.



**Example videos have been provided for the user to test the AI model on.**


---

## How to use

- After pasting the link in your web browser, you should see a simple UI.
  
- On the left, there is a box where you can upload a thermal video of the machinery you want to check.
  There are different videos provided in the `Videos for testing` folder for you to choose from.

- After uploading your desired video, you can the confidence threshold and the IoU to your desired levels and submit the video for inference.

- After some time, you will recieve the output in the form of a GIF that will show what the AI model thinks the issue is with any potential solutions.

- If there are any abnormalities, you can choose to **flag** the output. After flagging, this output will be stored in the `flagged` folder in the thermo-detect directory for later access.

---

## Important terms to know about

- What is confidence threshold?

  This score, typically ranging from 0 to 1 (or 0% to 100%), represents how certain the model is that an object of a particular class actually exists within that bounding box. A score of 1 means the model is highly certain, while a score closer to 0 means it's very uncertain.

  How it's used: The confidence threshold is a user-defined value (e.g., 0.25, 0.5, 0.7) that determines the minimum confidence score a detection must have to be considered valid and displayed.

    - Higher Threshold (e.g., 0.8): You'll get fewer detections, but the ones you do get will be highly certain. This reduces false positives (the model saying something is there when it isn't), leading to higher precision. However, it might also miss some actual objects that the model was less certain about (lower recall).
    - Lower Threshold (e.g., 0.2): You'll get more detections, including less certain ones. This increases recall (fewer missed objects) but might also increase false positives (more "ghost" detections or incorrect classifications), leading to lower precision.
 


- What is IoU threshold?

  Intersection over Union (IoU) is a metric used to quantify the overlap between two bounding boxes

  - Higher IoU Threshold (e.g., 0.75): Stricter requirement for a correct detection, leading to more emphasis on precise localization i.e more precision, less boxes
  - Lower IoU Threshold (e.g., 0.5): More lenient, allowing for slightly less precise bounding boxes to still be considered correct i.e. less precision, more boxes

---

## Acknowledgements

- The model on which Thermal Detect is based on is the Yolo V8 model by [Ultralytics](https://github.com/ultralytics/ultralytics)

---
