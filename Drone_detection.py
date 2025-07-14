import cv2
import torch
import numpy as np
from PIL import Image

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', source='github')

# Set video source (webcam)
cap = cv2.VideoCapture(0)

# Define the classes you want to detect
classes = ['Drone']

# Initialize the rectangle coordinates (top-left to bottom-right)
rectangle_coords = [(100, 100), (400, 100), (400, 400), (100, 400)]
rectangle_drag = False
drag_corner = -1

# Function to handle mouse events
def mouse_event(event, x, y, flags, param):
    global rectangle_coords, rectangle_drag, drag_corner

    if event == cv2.EVENT_LBUTTONDOWN:
        for i, corner in enumerate(rectangle_coords):
            if abs(corner[0] - x) <= 10 and abs(corner[1] - y) <= 10:
                rectangle_drag = True
                drag_corner = i
                break
    elif event == cv2.EVENT_LBUTTONUP:
        rectangle_drag = False
    elif event == cv2.EVENT_MOUSEMOVE and rectangle_drag:
        rectangle_coords[drag_corner] = (x, y)

# Create a window and set mouse callback
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', mouse_event)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not accessible")
        break

    # Convert to PIL Image for YOLOv5
    img = Image.fromarray(frame[..., ::-1])

    # YOLOv5 inference
    results = model(img, size=640)

    # Draw detections
    for result in results.xyxy[0]:
        x1, y1, x2, y2, conf, cls = result.tolist()
        if conf > 0.5 and classes[int(cls)] in classes:
            # Bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

            # Confidence and coordinates
            text_conf = "{:.2f}%".format(conf * 100)
            text_coords = "({}, {})".format(int((x1 + x2) / 2), int(y2))
            cv2.putText(frame, text_conf, (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.putText(frame, text_coords, (int(x1), int(y2) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Restricted zone logic
            rx1, ry1 = rectangle_coords[0]
            rx2, ry2 = rectangle_coords[2]
            if any(rx1 <= x <= rx2 and ry1 <= y <= ry2 for x, y in [(x1, y1), (x2, y2), (x1, y2), (x2, y1)]):
                cv2.putText(frame, "Warning: Drone Detected in Restricted Area!", (50, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Draw the rectangle
    for i in range(4):
        cv2.circle(frame, rectangle_coords[i], 5, (0, 255, 0), -1)
        cv2.line(frame, rectangle_coords[i], rectangle_coords[(i + 1) % 4], (0, 255, 0), 2)

    # Display the area dimensions
    width = rectangle_coords[1][0] - rectangle_coords[0][0]
    height = rectangle_coords[2][1] - rectangle_coords[1][1]
    cv2.putText(frame, f"Area: {width}x{height}", (rectangle_coords[0][0], rectangle_coords[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('frame', frame)

    # Keyboard controls
    key = cv2.waitKey(1) & 0xFF

    # Scale up with '+' or '='
    if key == ord('+') or key == ord('='):
        rx1, ry1 = rectangle_coords[0]
        rx2, ry2 = rectangle_coords[2]
        frame_h, frame_w = frame.shape[:2]
        rx1 = max(0, rx1 - 10)
        ry1 = max(0, ry1 - 10)
        rx2 = min(frame_w - 1, rx2 + 10)
        ry2 = min(frame_h - 1, ry2 + 10)
        rectangle_coords = [(rx1, ry1), (rx2, ry1), (rx2, ry2), (rx1, ry2)]

    # Scale down with '-' or '_'
    elif key == ord('-') or key == ord('_'):
        rx1, ry1 = rectangle_coords[0]
        rx2, ry2 = rectangle_coords[2]
        if rx2 - rx1 > 40 and ry2 - ry1 > 40:
            rx1 += 10
            ry1 += 10
            rx2 -= 10
            ry2 -= 10
            rectangle_coords = [(rx1, ry1), (rx2, ry1), (rx2, ry2), (rx1, ry2)]

    # Quit
    elif key == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
