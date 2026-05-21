# Rasoi Smriti - Indian Recipe Vault 🍳

A mobile-responsive web application designed for Indian households to preserve forgotten recipes, track cooking frequencies, and solve daily decision fatigue using **Python**, **Streamlit**, and **SQLite**.

---

## Features

1. **🔮 Dadi's Kitchen Oracle**: A smart decision fatigue solver that randomly suggests a traditional recipe that has not been cooked in the last 30 days. Clicking "We cooked this today!" resets its 30-day active timer.
2. **🔴 Forgotten recipe tracking**: Tracks and alerts you visually of recipe statuses:
   - 🔴 **Forgotten** (Not cooked in 30+ days)
   - 🟡 **Nearing Forgotten** (Not cooked in 20-29 days)
   - 🟢 **Active** (Cooked within the last 20 days)
3. **🗂️ Recipe Vault**: Search, browse, and filter recipes by region, category, ingredients, and status. It supports inline updates, quick logging, and edits.
4. **➕ Recipe Preservation**: A clean form to document family ingredients, categories, notes/memories, and cooking dates.
5. **📊 Insights Dashboard**: View bar charts showing distribution of dishes by region and category, along with stats on forgotten vs. active recipes.
6. **🌱 Automatic Seeding**: The app comes pre-seeded with 6 classic regional recipes (e.g., *Masala Dosa*, *Sarson Ka Saag*, *Litti Chokha*) representing the North, South, East, and West of India, with realistic offsets in dates so you can test all features immediately.

---

## Setup & Running Locally

### 1. Prerequisites
Make sure you have **Python 3.8+** installed.

### 2. Install Dependencies
Navigate to the project directory and run:
```bash
pip install -r requirements.txt
```

### 3. Launch the Application
Run the Streamlit application:
```bash
streamlit run app.py
```

Streamlit will open the application in your default web browser (typically at `http://localhost:8501`).

---

## Database Architecture
The application uses an SQLite database (`recipes.db`) created automatically inside the root folder on the first launch. 

### Schema:
* **id**: Unique identifier (integer auto-increment)
* **name**: Title of the recipe (text)
* **ingredients**: Comma-separated list of ingredients (text)
* **category**: E.g., Main Course, Breakfast, Dessert, Snack (text)
* **region**: E.g., North/South/East/West India (text)
* **last_cooked_date**: ISO date string `YYYY-MM-DD` (text)
* **notes**: Cooking instructions, secret family notes, or history (text)
