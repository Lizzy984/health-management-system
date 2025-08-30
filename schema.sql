-- Recipes table
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    ingredients TEXT NOT NULL,
    instructions TEXT NOT NULL,
    prep_time INTEGER,
    cook_time INTEGER,
    difficulty TEXT CHECK(difficulty IN ('easy', 'medium', 'hard')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Nutrition facts table
CREATE TABLE nutrition (
    id INTEGER PRIMARY KEY,
    food_item TEXT NOT NULL,
    calories INTEGER,
    protein REAL,
    carbohydrates REAL,
    fats REAL,
    fiber REAL,
    sugar REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Educational content table
CREATE TABLE educational_content (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    category TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Users table (for future expansion)
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    dietary_preferences TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);