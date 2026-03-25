from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from gtts import gTTS
import os
import requests
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Eco-Empath')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "No text received"}), 400

        text = data['text']
        print("Received:", repr(text))

        # Emotion detection
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity
        subjectivity = analysis.sentiment.subjectivity

        # Emotion logic
        if polarity > 0.5:
            emotion = "Excited 🤩"
            suggestion = "Channel your energy into something creative 🚀"
        elif polarity > 0.2:
            emotion = "Happy 😊"
            suggestion = "Keep smiling! Share your positivity 💛"
        elif -0.2 <= polarity <= 0.2:
            if subjectivity > 0.6:
                emotion = "Calm 😌"
                suggestion = "Try meditation or enjoy peaceful music 🧘"
            else:
                emotion = "Neutral 😐"
                suggestion = "Stay balanced and focused 💡"
        elif polarity < -0.5:
            emotion = "Angry 😡"
            suggestion = "Take a pause and breathe deeply 🌬️"
        elif polarity < -0.2:
            if subjectivity > 0.6:
                emotion = "Stressed 😰"
                suggestion = "Take a short break and relax 🌿"
            else:
                emotion = "Sad 😢"
                suggestion = "Talk to someone or take rest 💙"
        else:
            emotion = "Fearful 😨"
            suggestion = "Stay calm and focus on what you can control 🌱"

        # ✅ CREATE AUDIO
        os.makedirs("static", exist_ok=True)
        response_text = f"You are feeling {emotion}. {suggestion}"
        
        tts = gTTS(text=response_text, lang='en')
        
        # Consistent variable naming
        audio_filename = f"output_{int(time.time())}.mp3"
        audio_path = os.path.join("static", audio_filename)
        tts.save(audio_path)

        # ✅ FINAL RESPONSE (Fixed the variable reference here)
        return jsonify({
            "emotion": emotion,
            "suggestion": suggestion,
            "audio": f"/static/{audio_filename}" 
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)