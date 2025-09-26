from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.emotion_model import EmotionModel
from models.risk_model import RiskModel
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindmate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# DB models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    emotion = db.Column(db.String(100))
    risk = db.Column(db.Float)

# Load models
emotion_model = EmotionModel()
risk_model = RiskModel()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data.get('user_id', 1)
    text = data['text']

    # 1. Emotion detection
    emotion, emotion_probs = emotion_model.predict(text)

    # 2. Save message
    msg = Message(user_id=user_id, text=text, emotion=emotion)
    db.session.add(msg)
    db.session.commit()

    # 3. Recompute risk (last 10 messages)
    history = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp.desc()).limit(10).all()
    texts = [m.text for m in reversed(history)]
    risk_score = risk_model.predict(texts)

    msg.risk = float(risk_score)
    db.session.commit()

    # 4. Generate reply (simple rule-based MVP)
    if 'sad' in emotion.lower() or risk_score > 0.7:
        reply = "I’m sorry you’re feeling this way. Want to talk more? If you're in danger, contact local emergency services."
    else:
        reply = "Thanks for sharing. Tell me more — what happened today?"

    return jsonify({
        'reply': reply,
        'emotion': emotion,
        'risk': risk_score
    })

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    messages = Message.query.filter_by(user_id=user_id).order_by(Message.timestamp).all()
    data = [{'text':m.text, 't':m.timestamp.isoformat(), 'emotion':m.emotion, 'risk':m.risk} for m in messages]
    return render_template('dashboard.html', data=data)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
