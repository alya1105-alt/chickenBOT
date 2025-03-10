from ultralytics import YOLO
import cv2
import torch


device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")



model = YOLO("best.pt")  
model.to(device)  


cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    
    results = model(frame, device=device)  

    
    healthy_count = 0
    sick_count = 0

    
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  
            conf = box.conf[0].item()  
            cls = int(box.cls[0])  
           
            class_name = model.names[cls]  

            
            if class_name == "healthy":
                healthy_count += 1
            elif class_name == "sick":
                sick_count += 1

            
            label = f"{class_name} {conf:.2f}"
            color = (0, 255, 0) if class_name == "healthy" else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    
    cv2.putText(frame, f"Healthy: {healthy_count}  Sick: {sick_count}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

  
    cv2.imshow("YOLOv8 Chicken Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
