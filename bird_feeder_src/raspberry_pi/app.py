from flask import Flask, render_template, redirect, url_for, request
import json
import os
import requests  # ✅ Required for Wikipedia API calls

app = Flask(__name__)
DATA_FILE = 'bird_data.json'

# 🧠 Function to fetch image from Wikipedia
def get_bird_image_url(bird_name):
    search_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{bird_name.replace(' ', '_')}"
    response = requests.get(search_url)

    if response.status_code == 200:
        data = response.json()
        if "thumbnail" in data:
            return data["thumbnail"]["source"]
    return None

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    birds = data.get("birds", [])

    # 🔁 Add internet image to each bird
    for bird in birds:
        bird["internet_image"] = get_bird_image_url(bird["name"])

    return render_template('index.html', birds=birds)

@app.route('/delete/<timestamp>', methods=['POST'])
def delete_bird(timestamp):
    data = load_data()
    new_birds = []
    for bird in data["birds"]:
        if bird["timestamp"] == timestamp:
            if os.path.exists(bird["image_path"]):
                os.remove(bird["image_path"])
        else:
            new_birds.append(bird)
    data["birds"] = new_birds
    save_data(data)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
