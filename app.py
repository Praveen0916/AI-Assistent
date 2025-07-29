from flask import Flask, request, jsonify, render_template
import openai
import datetime
import wikipedia
import random
import webbrowser
import os

app = Flask(__name__)

# IMPORTANT: Never expose your OpenAI API key in public repos or shared code.
# For demo purposes only; use environment variables or config files in production.
openai.api_key = "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"

# Fixed joke list with commas separating items
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why do Java developers wear glasses? Because they don’t see sharp.",
    "I told my computer I needed a break, and it said: “No problem, I’ll go to sleep.”",
    "Why was the computer cold? It left its Windows open!",
    "How many programmers does it take to change a light bulb? None, that’s a hardware problem.",
    "Debugging: Being the detective in a crime movie where you are also the murderer.",
    "Why do Python programmers have low self-esteem? Because they’re constantly comparing their self to others.",
    "There are 10 types of people in the world: those who understand binary and those who don’t.",
    "Why did the programmer quit his job? Because he didn’t get arrays.",
    "Real programmers count from 0."
]

@app.route('/')
def index():
    # Render the main UI, assistant name is "Ghost"
    return render_template('index1.html', assistant_name="Ghost")

@app.route('/process', methods=['POST'])

def process_command():
    command = request.form.get('command', '').lower().strip()
    if not command:
        return jsonify({'response': "I didn't catch that. Please say something."})

    # 1. Respond with current time
    if "time" in command:
        now = datetime.datetime.now()
        return jsonify({'response': f"The current time is {now.strftime('%I:%M %p')}."})

    # 2. Respond with current date
    if "date" in command:
        today = datetime.date.today()
        return jsonify({'response': f"Today's date is {today.strftime('%B %d, %Y')}."})

    # 3. Wikipedia search
    if "wikipedia" in command:
        try:
            topic = command.replace("wikipedia", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            return jsonify({'response': summary})
        except Exception:
            return jsonify({'response': "Sorry, I couldn't find anything on Wikipedia for that."})

    # 4. Tell a joke
    if "joke" in command:
        return jsonify({'response': random.choice(jokes)})

    # 5. Open popular websites
    if "open youtube" in command:
        url = "https://www.youtube.com"
        webbrowser.open(url)
        return jsonify({'response': "Opening YouTube for you."})

    if "open google" in command:
        url = "https://www.google.com"
        webbrowser.open(url)
        return jsonify({'response': "Opening Google."})

    # 6. Play music (placeholder - update path as needed)
    if "play music" in command:
        music_path = "/path/to/your/music/folder"  # Change to your local music folder path
        try:
            os.startfile(music_path)
            return jsonify({'response': "Playing your music now."})
        except Exception:
            return jsonify({'response': "Sorry, I couldn't play music right now."})

    # 7. Take screenshot (only works if server has GUI)
    if "screenshot" in command:
        try:
            from PIL import ImageGrab
            filename = "screenshot.png"
            img = ImageGrab.grab()
            img.save(filename)
            return jsonify({'response': "Screenshot taken and saved as screenshot.png"})
        except Exception:
            return jsonify({'response': "Sorry, I couldn't take a screenshot."})
        # 9. Shutdown system
    if "shutdown system" in command:
        os.system("shutdown /s /t 1")
        return jsonify({'response': "Shutting down the system."})

    # 10. Restart system
    if "restart system" in command:
        os.system("shutdown /r /t 1")
        return jsonify({'response': "Restarting the system."})

    # 11. Lock the screen
    if "lock screen" in command:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return jsonify({'response': "Locking the screen."})

    # 12. Open Notepad
    if "open notepad" in command:
        os.system("start notepad")
        return jsonify({'response': "Opening Notepad."})

    # 13. Open Calculator
    if "open calculator" in command:
        os.system("start calc")
        return jsonify({'response': "Opening Calculator."})

    # 14. Open Command Prompt
    if "open command" in command or "open cmd" in command:
        os.system("start cmd")
        return jsonify({'response': "Opening Command Prompt."})

    # 15. Open Camera (Windows 10+)
    if "open camera" in command:
        os.system("start microsoft.windows.camera:")
        return jsonify({'response': "Opening Camera."})

    # 16. Open Chrome
    if "open chrome" in command:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        try:
            os.startfile(chrome_path)
            return jsonify({'response': "Opening Google Chrome."})
        except Exception:
            return jsonify({'response': "Could not open Chrome. Make sure the path is correct."})

    # 8. Use OpenAI GPT for other queries
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are Ghost, a helpful AI assistant."},
                {"role": "user", "content": command},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        assistant_reply = response['choices'][0]['message']['content'].strip()
    except Exception:
        assistant_reply = "Sorry, I couldn't process your request at the moment."

    return jsonify({'response': assistant_reply})

if __name__ == "__main__":
    app.run(debug=True)
