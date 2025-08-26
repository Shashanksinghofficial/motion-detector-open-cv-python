import cv2
import numpy as np
from twilio.rest import Client
import time

# Twilio की जानकारी
# इसे अपने Twilio अकाउंट के Account SID और Auth Token से बदलें
ACCOUNT_SID = ''# sid
AUTH_TOKEN = ''# Twilio का WhatsApp नंबर
TWILIO_WHATSAPP_NUMBER = 'whatsapp:+14155238886' # यह Twilio का Sandbox नंबर है
# आपका मोबाइल नंबर
YOUR_PHONE_NUMBER = 'whatsapp:+9184390000'  # अपना WhatsApp नंबर यहाँ डालें (देश कोड के साथ)

# Twilio क्लाइंट को इनिशियलाइज़ करें
client = Client(ACCOUNT_SID, AUTH_TOKEN)

# नोटिफिकेशन भेजने का फंक्शन
def send_whatsapp_notification(message):
    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=YOUR_PHONE_NUMBER
        )
        print("WhatsApp notification sent successfully!")
    except Exception as e:
        print(f"Error sending WhatsApp notification: {e}")

# वेबकैम शुरू करें
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# पहले फ्रेम को कैप्चर करें
ret, frame1 = cap.read()
if not ret:
    print("Error: Could not read frame from webcam.")
    exit()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

last_notification_time = 0
notification_cooldown = 1 # 30 सेकंड का कूलडाउन, ताकि बार-बार मैसेज न आए

while True:
    ret, frame2 = cap.read()
    if not ret:
        print("End of video stream.")
        break
    
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    diff = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame2, "Motion Detected!", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        motion_detected = True

    # अगर मोशन डिटेक्ट हुआ है और कूलडाउन खत्म हो गया है, तो नोटिफिकेशन भेजें
    if motion_detected and (time.time() - last_notification_time) > notification_cooldown:
        send_whatsapp_notification("Alert: Motion detected in front of the camera!")
        last_notification_time = time.time()

    cv2.imshow("Webcam Feed", frame2)
    
    gray1 = gray2

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()