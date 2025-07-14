# 🚁 Real-Time Drone Detection System with Restricted Zone Monitoring

This project is a real-time drone detection and intrusion alert system using **YOLOv5**, **OpenCV**, and **Python**. It allows users to define a dynamic "no-fly zone" and displays an alert if a drone is detected within that region using webcam feed.

📌 This project was built during my internship at **DRDO**, aiming to explore AI-driven surveillance systems for defense and monitoring applications.

---

## 🔍 Features

- 🧠 Real-time object detection using a YOLOv5 model
- 📷 Webcam-based video input (no external drone/camera needed)
- 🔲 Adjustable restricted area (draggable corners or `+` / `-` to resize)
- 🚨 Alerts when drone enters the restricted zone
- 💻 Fully runs on a local machine (Mac/Windows/Linux)

---

## 📁 File Structure

drone-detection/
├── drone_detection.py # Main script
├── best.pt # Trained YOLOv5 model (replace with yours)
├── requirements.txt # Python dependencies
├── README.md


---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/tanishkdagar20/Drone-Detection.git
cd drone-detection

### 2. Create and Activate Virtual Environment (Recommended)
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Add Trained YOLOv5 Model
Place your trained best.pt model file in the root directory.
Make sure the class in your model matches 'Drone'. You can update this in the script if needed.

🚀 Running the Project

python3 drone_detection.py
🎮 Controls

Action	Input
🛑 Exit program	q key
➕ Enlarge area	+ key
➖ Shrink area	- key
🖱️ Resize corners	Drag using mouse
🧠 Model Info

This script uses:

torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', source='github')
You can also clone YOLOv5 manually and switch to:

torch.hub.load('./yolov5', 'custom', path='best.pt', source='local')

____

##**🙋‍♂️ Author**

Tanishk Dagar
🛡️ DRDO Research Intern | 👨‍💻 AI/ML Enthusiast
Feel free to connect on LinkedIn
