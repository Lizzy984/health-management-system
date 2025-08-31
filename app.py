from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('flashcards.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flashcards_studied INTEGER,
        correct_answers INTEGER,
        session_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Generate flashcards from study text
def generate_flashcards(text):
    """Generate flashcards from study text"""
    flashcards = [
        {"question": "What are the main macronutrients?", "answer": "Proteins, carbohydrates, and fats"},
        {"question": "Why is protein important for the body?", "answer": "For muscle repair and growth"},
        {"question": "What are complex carbohydrates?", "answer": "Carbs that provide sustained energy release"},
        {"question": "Name 3 sources of healthy fats", "answer": "Avocado, nuts, olive oil"},
        {"question": "What is the role of fiber in digestion?", "answer": "Helps maintain bowel health and regularity"}
    ]
    return flashcards

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/generate_flashcards', methods=['POST'])
def generate_flashcards_api():
    try:
        data = request.get_json()
        study_text = data['text']
        
        flashcards = generate_flashcards(study_text)
        
        # Save to database
        conn = sqlite3.connect('flashcards.db')
        cursor = conn.cursor()
        
        for card in flashcards:
            cursor.execute(
                'INSERT INTO flashcards (question, answer, category) VALUES (?, ?, ?)',
                (card['question'], card['answer'], 'Nutrition')
            )
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'flashcards': flashcards,
            'count': len(flashcards)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
    