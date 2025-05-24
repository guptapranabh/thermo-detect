# thermo-detect

**A smart thermal imaging system to detect overheating components, identify the root cause, and provide actionable diagnostics.**

---

## Index

- [Overview](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#overview)
- [Features](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#features)
- [What the current project can/cannot do](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#what-the-current-project-cancannot-do)
- [Getting started](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#getting-started)
- [Installation](https://github.com/guptapranabh/thermo-detect?tab=readme-ov-file#installation-and-running)

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

## Acknowledgements

- The model on which Thermal Detect is based is the Yolo V8 model by [Ultralytics](https://github.com/ultralytics/ultralytics)

---
