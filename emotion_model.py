# models/emotion_model.py
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class EmotionModel:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def predict(self, text):
        # Vader sentiment
        vs = self.analyzer.polarity_scores(text)
        compound = vs['compound']

        # TextBlob polarity
        tb = TextBlob(text)
        polarity = tb.sentiment.polarity

        # Determine emotion
        if compound >= 0.5 or polarity >= 0.3:
            emotion = "happy"
        elif compound <= -0.5 or polarity <= -0.3:
            emotion = "sad"
        elif -0.3 < compound < 0.3:
            emotion = "neutral"
        else:
            emotion = "mixed"

        return emotion, {"vader": compound, "textblob": polarity}
