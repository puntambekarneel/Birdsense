# 🐦 BirdSense – The Smart AI Bird Feeder

**BirdSense** is a smart bird feeder that automatically captures images and short videos of birds, identifies their species using **Google Gemini AI**, and shows all the details beautifully on a **Flask web dashboard**.  
It helps people enjoy birdwatching effortlessl.

---

## 🌱 Why I Made It
When I visited a relative’s farmhouse, I saw many birds but whenever I got close, they flew away.  
I realized I didn’t have time to sit for hours just to watch birds.  
That’s when I thought *why not make something that takes photos for me and reminds me when birds visit my garden?*  
That idea became **BirdSense**.

---

## ⚙️ What It Does
- Detects when a bird appears and captures **photos + 10-second videos**  
- Uses **Gemini AI** to identify the bird species  
- Saves details like name, habitat, and diet  
- Displays everything neatly on a **Flask dashboard**  
- Allows deleting blurred or common photos directly from the UI  
- Works on any device connected to the same Wi-Fi network  

---

## 🧰 Hardware & Software
**Recommended Setup**
- Raspberry Pi Zero 2 W (or any Pi with camera support)  
- Pi Camera Module / USB Webcam  
- Raspberry Pi OS Legacy (32-bit)  
- 16 GB+ microSD card  
- Wi-Fi connection  
- Power supply 5 V 2 A  

**Install Dependencies**

sudo apt update
sudo apt install python3-pip python3-opencv python3-picamera ffmpeg -y
pip3 install flask google-generativeai

🚀 Run It
Clone repo

Edit bird_detect.py:

``` python
genai.configure(api_key="YOUR_API_KEY_HERE")
```
🧠 How It Works
The camera keeps watching for movement.

When a bird appears, it captures an image and short video.

Gemini AI confirms it’s a bird and identifies it.

Bird info, photo, and video are saved to JSON and shown on the dashboard.


bash
Copy code
https://github.com/puntambekarneel/Birdsense.git

run app.py and bird_detect.py

Open your browser at:
```http://<raspberry-pi-ip>:5000```


🌍 Access from Any Device
Connect your phone or laptop to the same Wi-Fi as your Raspberry Pi and visit:

```http://<raspberry-pi-ip>:5000```

👦 Creator
Neel Puntambekar (Age 16)

“BirdSense helps people connect with nature — even if they don’t have time to wait for the birds.”
