from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# Download required NLTK resources only if not already available
nltk_packages = ['punkt', 'wordnet', 'stopwords']
for pkg in nltk_packages:
    try:
        nltk.data.find(f'tokenizers/{pkg}' if pkg == 'punkt' else f'corpora/{pkg}')
    except LookupError:
        nltk.download(pkg)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize NLP tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Knowledge base
knowledge_base = {
    "greetings": {
        "patterns": ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"],
        "responses": [
            "Hello! How can I assist you today?",
            "Hi there! What can I do for you?",
            "Welcome! How may I help you?"
        ]
    },
    "goodbye": {
        "patterns": ["bye", "goodbye", "see you", "later", "farewell"],
        "responses": [
            "Goodbye! Have a great day!",
            "Thank you for chatting with us. Goodbye!",
            "See you later! Don't hesitate to reach out if you have more questions."
        ]
    },
    "help": {
        "patterns": ["help", "support", "assistance", "can you help"],
        "responses": [
            "I can help with account issues, product information, order status, and general questions.",
            "I'm here to assist with your questions about our products and services.",
            "How can I help you today? I can provide information about orders, products, and more."
        ]
    },
    "account": {
        "patterns": ["account", "login", "password", "sign in", "register", "profile"],
        "responses": [
            "For account-related issues, please visit the 'My Account' section on our website.",
            "You can reset your password by clicking 'Forgot Password' on the login page.",
            "Account settings can be changed in the 'Profile' section of your account."
        ]
    },
    "order": {
        "patterns": ["order", "track", "shipping", "delivery", "status", "purchase"],
        "responses": [
            "You can check your order status in the 'My Orders' section of your account.",
            "For order inquiries, please have your order number ready.",
            "Shipping times vary by location. You'll receive a tracking email once your order ships."
        ]
    },
    "product": {
        "patterns": ["product", "item", "spec", "feature", "catalog", "inventory"],
        "responses": [
            "Our products come with a 30-day money-back guarantee.",
            "Product specifications can be found on each product's detail page.",
            "For product availability, please check the product page or contact our sales team."
        ]
    },
    "payment": {
        "patterns": ["payment", "pay", "credit card", "bill", "invoice", "refund"],
        "responses": [
            "We accept Visa, MasterCard, American Express, and PayPal.",
            "Payment issues can often be resolved by trying a different payment method.",
            "For payment-related questions, please contact our billing department."
        ]
    },
    "thanks": {
        "patterns": ["thank", "thanks", "appreciate", "grateful"],
        "responses": [
            "You're welcome! Is there anything else I can help with?",
            "Happy to help! Let me know if you have other questions.",
            "My pleasure! Don't hesitate to ask if you need anything else."
        ]
    }
}

default_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "I don't have information on that topic. Could you ask something else?",
    "I'm still learning. Could you try asking a different question?",
    "I didn't quite get that. Can you provide more details?",
    "That's an interesting question. Let me connect you with a human agent who can help."
]

# Preprocessing function
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    return ' '.join(tokens)

# Prepare TF-IDF data
categories = []
patterns = []

for category, data in knowledge_base.items():
    for pattern in data["patterns"]:
        categories.append(category)
        patterns.append(preprocess_text(pattern))

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(patterns)

# Generate chatbot response
def get_bot_response(user_message):
    processed_input = preprocess_text(user_message)
    input_vec = vectorizer.transform([processed_input])
    
    similarities = cosine_similarity(input_vec, X)
    max_score = np.max(similarities)
    
    if max_score > 0.3:
        best_match_idx = np.argmax(similarities)
        category = categories[best_match_idx]
        return random.choice(knowledge_base[category]["responses"])
    
    return random.choice(default_responses)

# API endpoint
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message.strip():
        return jsonify({'response': "Please type a message so I can help you."})
    
    bot_response = get_bot_response(user_message)
    return jsonify({'response': bot_response})

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
