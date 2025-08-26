
# 🟢 Step 1: Python Install karna

1. [Python.org](https://www.python.org/downloads/) se **Python 3.13 (Windows installer)** download kijiye.
2. Install karte time niche ek option aayega **“Add Python to PATH”** → isko ✅ check zaroor karna.
3. Install hone ke baad CMD kholo aur check karo:

   ```bat
   python --version
   ```

   Agar version aa gaya (e.g. Python 3.13.x), matlab install sahi hai ✅

---

# 🟢 Step 2: Project Folder Banana

1. Desktop ya Documents me ek folder banao:

   ```
   MotionDetector
   ```
2. Iske andar aapki script file hogi.

---

# 🟢 Step 3: Required Libraries Install karna

CMD me folder open karo aur ye commands run karo:

```bat
pip install opencv-python numpy twilio
```

Yeh teen library install honi chahiye bina error ke.

---

# 🟢 Step 4: Twilio WhatsApp Sandbox Setup

1. Twilio account banao → [https://www.twilio.com/](https://www.twilio.com/)
2. Login karke → **Messaging → Try it out → WhatsApp sandbox** par jao.
3. Wahan ek number dikhayega: `+14155238886` (Twilio ka sandbox number).
4. Uske niche ek **join code** milega (e.g. `join engine-orange`)

   * Apne WhatsApp se Twilio number `+14155238886` par ye message bhejo:

     ```
     join engine-orange
     ```
   * Ab aap opt-in ho gaye, matlab Twilio aapko message bhej sakta hai. ✅

---

# 🟢 Step 5: Script File Banana

1. `MotionDetector` folder ke andar ek file banao:

   ```
   motion_whatsapp.py
   ```
2. Isme ye code paste karo (basic version, aapka Twilio SID/Auth Token number ke sath):

```python
import cv2
import numpy as np
from twilio.rest import Client
import time

# ---- Twilio Account Info ----
ACCOUNT_SID = "YOUR_ACCOUNT_SID"
AUTH_TOKEN = "YOUR_AUTH_TOKEN"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"   # Twilio Sandbox number
YOUR_PHONE_NUMBER = "whatsapp:+91XXXXXXXXXX"       # Apna WhatsApp number with country code

# Twilio client
client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_whatsapp_notification(message):
    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=YOUR_PHONE_NUMBER
        )
        print("WhatsApp notification sent!")
    except Exception as e:
        print(f"Error: {e}")

# ---- Camera Setup ----
cap = cv2.VideoCapture(0)  # agar external cam use karte ho to 1 kar do

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

ret, frame1 = cap.read()
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

last_notification_time = 0
cooldown = 30  # seconds

while True:
    ret, frame2 = cap.read()
    if not ret:
        break
    
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    diff = cv2.absdiff(gray1, gray2)
    thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion = False
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)
        motion = True

    if motion and (time.time() - last_notification_time) > cooldown:
        send_whatsapp_notification("⚠️ Motion Detected on Camera!")
        last_notification_time = time.time()

    cv2.imshow("Motion Detector", frame2)
    gray1 = gray2

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
```

👉 Apna **Account SID** aur **Auth Token** Twilio console se copy karke paste karo.
👉 Apna WhatsApp number `YOUR_PHONE_NUMBER` me `"whatsapp:+91XXXXXXXXXX"` format me daalo.

---

# 🟢 Step 6: Script Run Karna

CMD me jao aur folder ke andar ye command chalao:

```bat
python motion_whatsapp.py
```

👉 Camera ka window open hoga.
👉 Jab bhi motion detect hoga, WhatsApp pe message aa jayega.
👉 Band karne ke liye window select karke `q` dabao.

---

# 🟢 Step 7: Easy Double-Click Run (Optional)

1. Notepad kholke ye likho:

```bat
@echo off
python "C:\Users\<YourName>\MotionDetector\motion_whatsapp.py"
pause
```

2. Isko save karo as:

   ```
   StartMotion.bat
   ```
3. Ab bas double-click karoge to script turant chalegi ✅

---
