# thermo-detect

**A smart thermal imaging system to detect overheating components, identify the root cause, and provide actionable diagnostics.**

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
- Visual output with boundiing boxes on overheating parts of the component
- Provides diagnostic report and actionable output

---

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

Run `run_linux.sh` on your linux terminal or paste the following set of commands in your console:

Make the shell file `run_linux.sh` executable by running the command below:
```bash
chmod +x ./run_linux.sh
```

After that, start the program by running the command below:
```bash
./run_linux.sh
```


Run `run_windows.bat` on your Windows system by simply double clicking on it.


This will open a terminal and start downloading all the neccessary dependencies and start a server, typically on port `http://127.0.0.1:7860/`

Copy and paste the link on your web browser and it should open a WebUI where you can interact with the program.
