import sqlite3
import datetime
import os

DB_NAME = "recipes.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            category TEXT,
            region TEXT,
            last_cooked_date TEXT,
            notes TEXT
        )
    ''')
    
    # Check if procedure column exists, if not add it (Migration)
    cursor.execute("PRAGMA table_info(recipes)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'procedure' not in columns:
        cursor.execute("ALTER TABLE recipes ADD COLUMN procedure TEXT")
        conn.commit()

    # Check if empty, then seed
    cursor.execute("SELECT COUNT(*) FROM recipes")
    count = cursor.fetchone()[0]
    today = datetime.date.today()

    if count == 0:
        seed_recipes = [
            (
                "Masala Dosa",
                "Rice, Urad Dal, Fenugreek Seeds, Potatoes, Mustard Seeds, Curry Leaves, Turmeric, Onions",
                "Breakfast",
                "South India",
                (today - datetime.timedelta(days=45)).isoformat(),
                "Crispy crepes filled with a spiced potato mash. Serve hot with coconut chutney and sambar.",
                "1. Soak rice and urad dal for 5 hours, then grind into a smooth batter. 2. Ferment the batter overnight for 8-12 hours. 3. Spread a ladle of batter on a hot greased tawa in circular motions to make a thin crepe. 4. Drizzle ghee, add potato masala mixture in the center, fold and serve hot with chutney."
            ),
            (
                "Sarson Ka Saag",
                "Mustard Greens, Spinach, Bathua Greens, Ginger, Garlic, Maize Flour, Ghee, Green Chilies",
                "Curry",
                "North India",
                (today - datetime.timedelta(days=10)).isoformat(),
                "A winter favorite from Punjab. Best paired with Makki Di Roti (corn flatbread) and white butter.",
                "1. Wash and chop mustard greens, spinach, and bathua greens. 2. Pressure cook greens with ginger, garlic, and green chilies. 3. Mash cook greens with maize flour (makki atta) to make it smooth. 4. Temper with onions, garlic, and generous amount of ghee."
            ),
            (
                "Hyderabadi Biryani",
                "Basmati Rice, Chicken/Paneer, Yogurt, Mint Leaves, Coriander, Fried Onions, Saffron, Ghee, Biryani Masala",
                "Main Course",
                "South India",
                (today - datetime.timedelta(days=32)).isoformat(),
                "A slow-cooked, layered aromatic rice dish. Traditional dum method is highly recommended.",
                "1. Marinate chicken or paneer in yogurt, ginger-garlic paste, mint, coriander, and biryani spices for 2 hours. 2. Parboil basmati rice with whole spices until 70% cooked. 3. Layer the marinated mixture and rice alternately in a heavy pot, topped with saffron milk, fried onions, and ghee. 4. Seal pot with dough/foil and dum-cook on low heat for 25 minutes."
            ),
            (
                "Gajar Ka Halwa",
                "Red Carrots, Whole Milk, Sugar, Khoya, Ghee, Cashews, Almonds, Green Cardamom Powder",
                "Dessert",
                "North India",
                (today - datetime.timedelta(days=25)).isoformat(),
                "Slow-cooked carrot pudding. Grating the carrots finely yields the best texture.",
                "1. Grate red carrots and cook them in whole milk on a medium flame until milk evaporates. 2. Add ghee and sauté the carrots for 10-15 minutes. 3. Add sugar, khoya, and cardomom powder, stirring constantly. 4. Garnish with chopped almonds and cashews before serving hot."
            ),
            (
                "Dhokla",
                "Gram Flour (Besan), Semolina, Ginger-Green Chili Paste, Eno Fruit Salt, Lemon Juice, Mustard Seeds, Fresh Coconut",
                "Snack",
                "West India",
                (today - datetime.timedelta(days=5)).isoformat(),
                "Soft, spongy, steamed savory cake. Tempered with mustard seeds, sesame, and curry leaves.",
                "1. Prepare batter by mixing gram flour (besan), water, lemon juice, ginger paste, and salt. 2. Just before steaming, stir in Eno fruit salt to make it frothy. 3. Pour into a greased pan and steam for 12-15 minutes. 4. Temper with mustard seeds, curry leaves, sesame, green chilies, and a splash of water, then pour over dhokla."
            ),
            (
                "Litti Chokha",
                "Whole Wheat Flour, Sattu (Roasted Gram Flour), Mustard Oil, Kalonji, Ajwain, Brinjal, Potatoes, Tomatoes, Garlic",
                "Main Course",
                "East India",
                (today - datetime.timedelta(days=60)).isoformat(),
                "A rustic traditional dish from Bihar. Littis are roasted over charcoal and dipped in warm ghee.",
                "1. Mix sattu with mustard oil, pickle masala, ginger, garlic, chilies, kalonji, and coriander. 2. Stuff the sattu mixture inside small wheat flour dough balls. 3. Roast littis over charcoal or in an oven at 200C. 4. Mash roasted eggplant, boiled potatoes, and tomatoes with mustard oil, garlic, and chilies to make chokha. Serve littis dipped in hot ghee."
            )
        ]
        cursor.executemany('''
            INSERT INTO recipes (name, ingredients, category, region, last_cooked_date, notes, procedure)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', seed_recipes)
        conn.commit()
    else:
        # Migration logic: update categories and procedures of seed recipes if they are not set
        seed_updates = [
            ("Masala Dosa", "Breakfast", "1. Soak rice and urad dal for 5 hours, then grind into a smooth batter. 2. Ferment the batter overnight for 8-12 hours. 3. Spread a ladle of batter on a hot greased tawa in circular motions to make a thin crepe. 4. Drizzle ghee, add potato masala mixture in the center, fold and serve hot with chutney."),
            ("Sarson Ka Saag", "Curry", "1. Wash and chop mustard greens, spinach, and bathua greens. 2. Pressure cook greens with ginger, garlic, and green chilies. 3. Mash cook greens with maize flour (makki atta) to make it smooth. 4. Temper with onions, garlic, and generous amount of ghee."),
            ("Hyderabadi Biryani", "Main Course", "1. Marinate chicken or paneer in yogurt, ginger-garlic paste, mint, coriander, and biryani spices for 2 hours. 2. Parboil basmati rice with whole spices until 70% cooked. 3. Layer the marinated mixture and rice alternately in a heavy pot, topped with saffron milk, fried onions, and ghee. 4. Seal pot with dough/foil and dum-cook on low heat for 25 minutes."),
            ("Gajar Ka Halwa", "Dessert", "1. Grate red carrots and cook them in whole milk on a medium flame until milk evaporates. 2. Add ghee and sauté the carrots for 10-15 minutes. 3. Add sugar, khoya, and cardomom powder, stirring constantly. 4. Garnish with chopped almonds and cashews before serving hot."),
            ("Dhokla", "Snack", "1. Prepare batter by mixing gram flour (besan), water, lemon juice, ginger paste, and salt. 2. Just before steaming, stir in Eno fruit salt to make it frothy. 3. Pour into a greased pan and steam for 12-15 minutes. 4. Temper with mustard seeds, curry leaves, sesame, green chilies, and a splash of water, then pour over dhokla."),
            ("Litti Chokha", "Main Course", "1. Mix sattu with mustard oil, pickle masala, ginger, garlic, chilies, kalonji, and coriander. 2. Stuff the sattu mixture inside small wheat flour dough balls. 3. Roast littis over charcoal or in an oven at 200C. 4. Mash roasted eggplant, boiled potatoes, and tomatoes with mustard oil, garlic, and chilies to make chokha. Serve littis dipped in hot ghee.")
        ]
        for name, cat, proc in seed_updates:
            cursor.execute("UPDATE recipes SET category = ?, procedure = ? WHERE name = ? AND (procedure IS NULL OR procedure = '')", (cat, proc, name))
        
        # Make sure any null procedure is set to a default string
        cursor.execute("UPDATE recipes SET procedure = 'No procedure documented yet.' WHERE procedure IS NULL")
        conn.commit()

    conn.close()

def get_all_recipes():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM recipes ORDER BY last_cooked_date ASC")
    rows = cursor.fetchall()
    conn.close()
    
    recipes = []
    for r in rows:
        recipe = dict(r)
        # Calculate days since last cooked
        last_cooked = datetime.date.fromisoformat(recipe['last_cooked_date'])
        days_since = (datetime.date.today() - last_cooked).days
        recipe['days_since_cooked'] = days_since
        recipe['status'] = "Forgotten" if days_since >= 30 else ("Nearing Forgotten" if days_since >= 20 else "Active")
        if 'procedure' not in recipe or recipe['procedure'] is None:
            recipe['procedure'] = "No procedure documented yet."
        recipes.append(recipe)
    return recipes

def get_forgotten_recipes():
    recipes = get_all_recipes()
    return [r for r in recipes if r['status'] == "Forgotten"]

def add_recipe(name, ingredients, category, region, last_cooked_date, notes, procedure):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO recipes (name, ingredients, category, region, last_cooked_date, notes, procedure)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, ingredients, category, region, last_cooked_date, notes, procedure))
    conn.commit()
    conn.close()

def update_recipe(recipe_id, name, ingredients, category, region, last_cooked_date, notes, procedure):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE recipes
        SET name = ?, ingredients = ?, category = ?, region = ?, last_cooked_date = ?, notes = ?, procedure = ?
        WHERE id = ?
    ''', (name, ingredients, category, region, last_cooked_date, notes, procedure, recipe_id))
    conn.commit()
    conn.close()

def mark_as_cooked_today(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    today_str = datetime.date.today().isoformat()
    cursor.execute('''
        UPDATE recipes
        SET last_cooked_date = ?
        WHERE id = ?
    ''', (today_str, recipe_id))
    conn.commit()
    conn.close()

def delete_recipe(recipe_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
    conn.commit()
    conn.close()
