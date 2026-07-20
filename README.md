# 🚗 AI Driver Monitoring System

A real-time AI-powered Driver Monitoring System that detects **fatigue**, **microsleep**, and **driver distraction** using Computer Vision and facial landmark analysis. The system provides live safety monitoring, audio alerts, event logging, and an interactive analytics dashboard.

---

## 📌 Project Overview

Road accidents caused by driver fatigue and distraction remain a major safety concern. This project continuously monitors a driver's face through a webcam and analyzes facial movements to detect unsafe driving behaviour.

The system identifies:

- 👁️ Blink Detection
- 😴 Microsleep Detection
- 🥱 Yawn Detection
- 🚘 Head Direction & Distraction Detection
- 📊 Driver Fatigue Analysis
- 🛡️ Safety Score Calculation
- 🔊 Real-Time Alarm System
- 💾 Trip Event Logging
- 📈 Analytics Dashboard

---

## ✨ Features

- Real-time webcam-based driver monitoring
- Facial landmark detection using MediaPipe Face Mesh
- Eye Aspect Ratio (EAR) based blink & microsleep detection
- Mouth Aspect Ratio (MAR) based yawn detection
- Head pose estimation using OpenCV solvePnP()
- Driver distraction detection (Left / Right / Up / Down)
- Driver safety score calculation
- Continuous alarm during dangerous situations
- SQLite database for trip event storage
- Interactive Streamlit dashboard
- Trip-wise event logging

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Computer Vision
- OpenCV
- MediaPipe

### Mathematical Processing
- NumPy

### Database
- SQLite

### Dashboard
- Streamlit
- Plotly

### Audio Alerts
- Pygame

---

## 📂 Project Structure

```text
AI-Driver-Monitoring-System
│
├── alerts/
│   └── alarm.py
│
├── analysis/
│   ├── distraction.py
│   ├── fatigue_analyzer.py
│   ├── microsleep.py
│   └── safety_score.py
│
├── assets/
│   └── alarm.wav
│
├── dashboard/
│   └── dashboard.py
│
├── database/
│   └── database_manager.py
│
├── detection/
│   ├── camera.py
│   ├── eye.py
│   ├── face_mesh.py
│   ├── head_pose.py
│   └── mouth.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

# 🏗️ System Architecture

```text
               Webcam
                  │
                  ▼
        OpenCV Video Capture
                  │
                  ▼
      MediaPipe Face Mesh (468 Landmarks)
                  │
        ┌─────────┼──────────┐
        ▼         ▼          ▼
      EAR        MAR     Head Pose
        │          │          │
        ▼          ▼          ▼
 Blink     Yawn Detection  Distraction
 Detection                  Detection
        │          │          │
        └──────────┼──────────┘
                   ▼
          Fatigue Analysis
                   ▼
           Safety Score Engine
                   ▼
      Alarm + Event Logging
                   ▼
          SQLite Database
                   ▼
       Streamlit Dashboard
```

---

# 🧠 Detection Modules

## 👁️ Blink Detection

The system calculates the **Eye Aspect Ratio (EAR)** using MediaPipe facial landmarks.

When the EAR falls below a threshold and returns back to normal, a blink event is detected.

---

## 😴 Microsleep Detection

Microsleep is detected when the driver's eyes remain closed continuously for a predefined number of frames.

During microsleep:

- Alarm starts
- Safety score decreases
- Event is stored in the database

---

## 🥱 Yawn Detection

The system computes the **Mouth Aspect Ratio (MAR)**.

If the MAR exceeds a threshold, a yawn event is detected.

---

## 🚘 Distraction Detection

Head pose estimation is performed using OpenCV's `solvePnP()`.

The driver is classified as:

- Looking Left
- Looking Right
- Looking Up
- Looking Down
- Looking Forward

---

## 🛡️ Safety Score

The driver starts with a score of **100**.

The score decreases based on:

- Frequent blinking
- Yawning
- Microsleep
- Driver distraction

The system classifies the driver's condition as:

- Excellent
- Good
- Alert
- Danger

---
