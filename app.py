# app.py (Python Backend)
from flask import Flask, render_template, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('nourishlearn.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 email TEXT UNIQUE NOT NULL,
                 age INTEGER,
                 gender TEXT,
                 weight REAL,
                 height REAL,
                 activity_level TEXT)''')
    
    # Create nutrition logs table
    c.execute('''CREATE TABLE IF NOT EXISTS nutrition_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id INTEGER,
                 date TEXT NOT NULL,
                 calories INTEGER,
                 protein REAL,
                 carbs REAL,
                 fats REAL,
                 FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # Create educational resources table
    c.execute('''CREATE TABLE IF NOT EXISTS resources
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 category TEXT NOT NULL,
                 content TEXT,
                 url TEXT)''')
    
    # Insert sample resources
    sample_resources = [
        ('Balanced Diet Fundamentals', 'Nutrition', 
         'Learn about the five food groups and how to create balanced meals...', 
         '/resources/balanced-diet'),
        ('Sustainable Farming Practices', 'Agriculture', 
         'Discover methods to grow food sustainably and reduce environmental impact...', 
         '/resources/sustainable-farming'),
        ('Meal Planning on a Budget', 'Cooking', 
         'Tips for creating nutritious meals without breaking the bank...', 
         '/resources/budget-meals')
    ]
    
    c.executemany('INSERT OR IGNORE INTO resources (title, category, content, url) VALUES (?, ?, ?, ?)', 
                  sample_resources)
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    conn = sqlite3.connect('nourishlearn.db')
    c = conn.cursor()
    
    try:
        c.execute('''INSERT INTO users (name, email, age, gender, weight, height, activity_level)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (data['name'], data['email'], data['age'], data['gender'], 
                  data['weight'], data['height'], data['activity_level']))
        conn.commit()
        user_id = c.lastrowid
        return jsonify({'success': True, 'user_id': user_id})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Email already exists'})
    finally:
        conn.close()

@app.route('/api/nutrition/<user_id>', methods=['GET'])
def get_nutrition(user_id):
    conn = sqlite3.connect('nourishlearn.db')
    c = conn.cursor()
    
    # Get user data
    c.execute('SELECT age, gender, weight, height, activity_level FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'})
    
    age, gender, weight, height, activity_level = user
    
    # Calculate nutritional needs (same logic as frontend)
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very-active': 1.9
    }
    
    calories = round(bmr * activity_multipliers.get(activity_level, 1.2))
    protein = round(weight * 1.6)
    carbs = round((calories * 0.5) / 4)
    fats = round((calories * 0.3) / 9)
    
    return jsonify({
        'success': True,
        'calories': calories,
        'protein': protein,
        'carbs': carbs,
        'fats': fats
    })

@app.route('/api/resources')
def get_resources():
    category = request.args.get('category', '')
    conn = sqlite3.connect('nourishlearn.db')
    c = conn.cursor()
    
    if category:
        c.execute('SELECT id, title, category, content, url FROM resources WHERE category = ?', (category,))
    else:
        c.execute('SELECT id, title, category, content, url FROM resources')
    
    resources = []
    for row in c.fetchall():
        resources.append({
            'id': row[0],
            'title': row[1],
            'category': row[2],
            'content': row[3],
            'url': row[4]
        })
    
    conn.close()
    return jsonify(resources)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)