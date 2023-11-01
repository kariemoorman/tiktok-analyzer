#!/usr/bin/python3

import re
import json
import numpy as np
import spacy

nlp = spacy.load("en_core_web_md")

emotion_adjs = [
    "Happy", "Sad", "Angry", "Excited", "Fearful", "Confident", "Relaxed", "Anxious", 
    "Joyful", "Depressed", "Grateful", "Content", "Enthusiastic", "Worried", "Surprised", 
    "Nervous", "Frustrated", "Proud", "Curious", "Hopeful", "Lonely", "Optimistic", "Rude",
    "Overwhelmed", "Irritated", "Amazed", "Disappointed", "Guilty", "Jealous", "Confused", 
    "Loved", "Hated", "Indifferent", "Ecstatic", "Embarrassed", "Insecure", "Sympathetic", 
    "Apathetic", "Pleased", "Skeptical", "Overjoyed", "Elated", "Discontent", "Resentful",
    "Cautious", "Blissful", "Regretful", "Enraged", "Hopeless", "Serene", "Apprehensive",
    "Melancholic", "Vengeful", "Bittersweet", "Inadequate", "Giddy", "Uneasy", "Grief-stricken",
    "Astonished", "Disgusted", "Satisfied", "Empathetic", "Disheartened", "Charmed", "Fulfilled",
    "Appalled", "Overcome", "Irrational", "Awestruck", "Baffled", "Aghast", "Tempted", "Desperate", 
    "Inspired", "Agitated", "Grumpy", "Indignant", "Paranoid", "Confounded", "Revived", "Envious",
    "Humbled", "Skeptical", "Smitten", "Despondent", "Uneasy", "Delighted", "Detached", "Delirious",
    "Shy", "Excited", "Lethargic", "Astonished", "Exhilarated", "Wistful", "Numb", "Playful", 
    "Hostile", "Cautious", "Grateful", "Enchanted", "Alienated", "Scared", "Fearful", "Petrified",
    "Caring", "Composed", "Considerate", "Ecstatic", "Enthusiastic", "Overwhelmed", "Radiant", 
    "Thoughtful", "Captivated", "Impulsive", "Devoted", "Zestful", "Inspired", "Rapturous", "Safe",
    "Reflective", "Desolate", "Desperate", "Flabbergasted", "Forlorn", "Heedless", "Hollow", "Unsafe",
    "Introspective", "Lively", "Malcontent", "Mournful", "Ominous", "Passionate", "Receptive", 
    "Scornful", "Sentimental", "Spellbound", "Unnerved", "Vexed", "Zealous", "Rad", "Awesome", "Obnoxious"
    ]

emotion_nouns = [
    "Love", "Hate", "Joy", "Sorrow", "Anger", "Fear", "Excitement", "Anxiety", "Happiness", "Sadness",
    "Frustration", "Contentment", "Envy", "Jealousy", "Rage", "Delight", "Disgust", "Affection", 
    "Grief", "Elation", "Guilt", "Shame", "Regret", "Hope", "Despair", "Surprise", "Anticipation", 
    "Curiosity", "Sympathy", "Empathy", "Awe", "Compassion", "Boredom", "Amusement", "Loneliness", 
    "Euphoria", "Apathy", "Tenderness", "Resentment", "Adoration", "Melancholy", "Nostalgia", "Satisfaction", 
    "Disappointment", "Wonder", "Worry", "Trepidation", "Apprehension", "Confusion", "Surprise", "Pity", 
    "Excitement", "Admiration", "Revulsion", "Regret", "Elation", "Discomfort", "Remorse", "Euphoria", 
    "Alienation", "Relief", "Disbelief", "Sympathy", "Hostility", "Empathy", "Triumph", "Desperation", 
    "Nostalgia", "Devotion", "Vulnerability", "Bitterness", "Indifference", "Loneliness", "Melancholy", 
    "Tenderness", "Compassion", "Frenzy", "Apathy", "Elation", "Embarrassment", "Yearning", "Satisfaction",
    "Guilt", "Remorse", "Bewilderment", "Astonishment", "Resignation", "Empowerment", "Disillusionment", 
    "Gratitude", "Alienation", "Contempt", "Adoration", "Obsession", "Disappointment", "Resilience", 
    "Synergy", "Excitation", "Isolation", "Bliss", "Fulfillment", "Jealousy", "Serenity", "Rejection", 
    "Hostility", "Confusion", "Sorrow", "Despair", "Nervousness"
    ]

emotion_verbs = [
    "Love", "Hate", "Laugh", "Cry", "Smile", "Frown", "Scream", "Shout", "Rejoice", "Mourn", "Calm", "Comfort", 
    "Console", "Cheer", "Sigh", "Tremble", "Worry", "Fear", "Rage", "Despair", "Long", "Crave", "Delight", "Envy", 
    "Jealousy", "Admire", "Awe", "Appreciate", "Grin", "Grieve", "Glare", "Celebrate", "Cherish", "Blush", "Startle", 
    "Sob", "Flinch", "Panic", "Relish", "Mope", "Confide", "Disgust", "Regret", "Sympathize", "Empathize", "Nod", 
    "Wince", "Whisper", "Apologize", "Cringe", "Sulk", "Cling", "Surrender", "Pray", "Revere", "Repulse", "Lament", 
    "Despise", "Hesitate", "Gasp", "Adore", "Dote", "Resent", "Long", "Pine", "Covet", "Embrace", "Abhor", "Clench", 
    "Crave", "Panic", "Plead", "Recoil", "Thrive", "Prevail", "Cherish", "Avenge", "Confront", "Yield", "Savor", 
    "Cherish", "Detest", "Astonish", "Recoil", "Sneer", "Flirt", "Panic", "Snicker", "Whimper", "Moan", "Swoon", "Recoil", 
    "Convulse", "Howl", "Stammer", "Quiver", "Surrender", "Wail", "Choke", "Crumble", "Stalk"
    ]

emotion_adjs = [word.lower() for word in emotion_adjs]
emotion_nouns = [word.lower() for word in emotion_nouns]
emotion_verbs = [word.lower() for word in emotion_verbs]

def filter_words(text):
    # Minor alterations using regex
    string = re.sub(r"(\bi\'m\b)", "i am", text)
    string = re.sub(r"(\bi\'ve\b)", "i have", string)
    string = re.sub(r"(\bisn\'t\b)", "is not", string)
    string = re.sub(r"(\bit\'s\b)", "it is", string)
    string = re.sub(r"(\bwe\'re\b)", "we are", string)
    string = re.sub(r"(\bdidn\'t\b)", "did not", string)
    string = re.sub(r"(\bcan\'t\b)", "cannot", string)
    string = re.sub(r"(\b(?<=[a-z])n't\b)", " not", string)
    string = re.sub(r"((?<=[a-z])\'d\b)", " would", string)
    string = re.sub(r"((?<=[a-z])\'s\b)", "", string)
    string = re.sub(r"[^\w\s]", "", string)
    # Lemmatize words
    doc = nlp(string.lower())
    lemmas = [token.lemma_ for token in doc if token.is_alpha and not token.is_punct]
    # Extract emotion words
    emotion_words = emotion_adjs + emotion_verbs + emotion_nouns
    emotion_list = [word for word in lemmas if word in emotion_words]
    return emotion_list
