from flask import Flask, render_template, request, jsonify
import datetime

app = Flask(__name__)

chat_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get", methods=["POST"])
def chatbot_response():
    user_message = request.json["message"].lower()

    # Rule-based logic
    if "hello" in user_message or "hi" in user_message:
        reply = "Hey! How can I help you?"
    elif "how are you" in user_message:
        reply = "I’m doing great 🤖 Thanks for asking!"
    elif "your name" in user_message:
        reply = "I’m ChatBot 1.0 — your rule-based buddy."
    elif "weather" in user_message:
        reply = "Hmm, I can't check weather yet, but I bet it’s nice where you are 🌤️"
    elif "joke" in user_message:
        reply = "Why don’t programmers like nature? Too many bugs 🐞😂"
    elif "bye" in user_message:
        reply = "Goodbye! Have a nice day!"
    elif "time" in user_message:
        reply = f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')} ⏰"
    elif "date" in user_message:
        reply = f"Today's date is {datetime.datetime.now().strftime('%Y-%m-%d')} 📅"
    elif "food" in user_message:
        reply = "I love pizza 🍕, but sadly I can’t eat 😅"
    elif "hobby" in user_message:
        reply = "My hobby? Chatting with you of course 💬"
    elif "language" in user_message:
        reply = "I speak Python 🐍 fluently. What about you?"
    elif "motivate" in user_message or "motivation" in user_message:
        reply = "Keep going! You’re smarter than you think, stronger than you feel, and braver than you believe 💪✨"
    else:
        reply = "Sorry, I don’t understand that."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
