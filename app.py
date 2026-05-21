import streamlit as st
import database as db
import random
import datetime
import pandas as pd
from google import genai

# Try loading the microphone recorder safely
try:
    from streamlit_mic_recorder import mic_recorder
except ImportError:
    st.error("📦 Please run 'pip install streamlit-mic-recorder' in your terminal.")

# Initialize Gemini Client using Streamlit secrets safely
try:
    client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.warning("🔑 Gemini API Key missing or incorrect in .streamlit/secrets.toml. AI processing will be disabled until fixed.")
    client = None

# Page configuration
st.set_page_config(
    page_title="Flavors of the Past - Indian Recipe Vault",
    page_icon="🍳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize database and seed if empty
db.init_db()

# State management
if 'suggested_recipe' not in st.session_state:
    st.session_state.suggested_recipe = None

if 'editing_recipe_id' not in st.session_state:
    st.session_state.editing_recipe_id = None

# Custom CSS Styling Injection
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,900;1,600&display=swap');

/* Global Font Overrides */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif !important;
}

/* Page Background */
.stApp {
    background-color: #FFFDF9 !important;
    color: #2F3E46 !important;
}

/* Hide default streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Header styling */
.header-container {
    text-align: center;
    padding: 1.5rem 0;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #FAF0E6 0%, #FFFDF9 100%);
    border-radius: 16px;
    border: 1px solid #F3E5D8;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.02);
}
.header-title {
    font-size: 2.5rem;
    font-weight: 900;
    margin: 0;
    background: linear-gradient(90deg, #E76F51 0%, #F4A261 50%, #81B29A 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header-subtitle {
    font-size: 1rem;
    color: #5C6B73;
    margin-top: 0.4rem;
    font-weight: 500;
}

/* Forgotten Gem Card */
.gem-card {
    background: linear-gradient(135deg, #FFFDF9 0%, #FAF5EF 100%);
    border: 2px solid #F4D3B5;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(231, 111, 81, 0.08);
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Recipe Card in Directory */
.recipe-card {
    background-color: #FFFFFF !important;
    border: 1px solid #EAE2D5 !important;
    border-radius: 12px !important;
    padding: 1.25rem !important;
    margin-bottom: 1rem !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.01) !important;
    transition: all 0.2s ease !important;
}
.recipe-card:hover {
    border-color: #F4A261 !important;
    box-shadow: 0 8px 16px rgba(231, 111, 81, 0.06) !important;
    transform: translateY(-2px) !important;
}

/* Badges */
.badge {
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-block;
}
.badge-forgotten {
    background-color: #FAD2E1;
    color: #7C1A22;
    border: 1px solid #F0A6B2;
}
.badge-nearing {
    background-color: #FFE5B4;
    color: #8A4F00;
    border: 1px solid #FFD384;
}
.badge-active {
    background-color: #D8F3DC;
    color: #1B4332;
    border: 1px solid #B7E4C7;
}

/* Ingredient tag */
.ingredient-tag {
    background-color: #FAF0E6;
    color: #5C6B73;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 0.35rem;
    margin-bottom: 0.35rem;
    display: inline-block;
    border: 1px solid #EAE2D5;
}

/* Streamlit Tabs Customization */
button[data-baseweb="tab"] {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color: #6D7A80 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #E76F51 !important;
    border-bottom-color: #E76F51 !important;
}

/* Button overrides */
.stButton > button, 
.stFormSubmitButton > button {
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.25rem !important;
    transition: all 0.2s ease-in-out !important;
    color: #FFFFFF !important;
}

/* Saffron Primary buttons */
.stButton > button[kind="primary"], 
.stButton > button[data-testid="stBaseButton-primary"],
.stFormSubmitButton > button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, #FF9933 0%, #E76F51 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(231, 111, 81, 0.25) !important;
}
.stButton > button[kind="primary"]:hover, 
.stButton > button[data-testid="stBaseButton-primary"]:hover,
.stFormSubmitButton > button[kind="primaryFormSubmit"]:hover {
    background: linear-gradient(135deg, #FFAA55 0%, #F4A261 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 15px rgba(231, 111, 81, 0.35) !important;
    transform: translateY(-1px) !important;
}

/* Sage Green Secondary/Default buttons */
.stButton > button,
.stButton > button[kind="secondary"], 
.stButton > button[data-testid="stBaseButton-secondary"],
.stFormSubmitButton > button,
.stFormSubmitButton > button[kind="secondaryFormSubmit"] {
    background: linear-gradient(135deg, #95C3A5 0%, #6BA283 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    box-shadow: 0 4px 10px rgba(107, 162, 131, 0.15) !important;
}
.stButton > button:hover,
.stButton > button[kind="secondary"]:hover, 
.stButton > button[data-testid="stBaseButton-secondary"]:hover,
.stFormSubmitButton > button:hover,
.stFormSubmitButton > button[kind="secondaryFormSubmit"]:hover {
    background: linear-gradient(135deg, #A3D1B3 0%, #81B29A 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 6px 15px rgba(107, 162, 131, 0.25) !important;
    transform: translateY(-1px) !important;
}

/* Make inputs look warm and clean */
.stTextInput input, .stTextArea textarea, .stDateInput input {
    background-color: #FFFFFF !important;
    border: 1px solid #EAE2D5 !important;
    border-radius: 8px !important;
    color: #2F3E46 !important;
}
.stTextInput input:focus, .stTextArea textarea:focus, .stDateInput input:focus {
    border-color: #F4A261 !important;
    box-shadow: 0 0 0 2px rgba(244, 162, 97, 0.2) !important;
}

/* Fallback box */
.fallback-box {
    text-align: center;
    padding: 2.5rem;
    background: rgba(129, 178, 154, 0.08);
    border: 2px dashed rgba(129, 178, 154, 0.4);
    border-radius: 16px;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}
.fallback-title {
    color: #4E8752;
    margin-top: 0.5rem;
    font-size: 1.5rem;
    font-weight: 700;
}
.fallback-text {
    color: #5C6B73;
    font-size: 0.95rem;
    margin-bottom: 0;
}

/* Heading spacers */
.form-section-header {
    margin-top: 1.25rem !important;
    margin-bottom: 0.75rem !important;
    color: #E76F51 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# Main Application Title
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🍳 Flavors of the Past</h1>
        <div class="header-subtitle">Indian Household Recipe Reminder App</div>
    </div>
""", unsafe_allow_html=True)

# Define exactly three tabs
tab1, tab2, tab3 = st.tabs([
    "🥗 What to Cook Today",
    "🗂️ Recipe Vault",
    "Add New Recipe 📝"
])

# ====================
# TAB 1: WHAT TO COOK TODAY (Homepage)
# ====================
with tab1:
    st.markdown("### 🔮 Forgotten Gems Oracle")
    st.write("Feeling undecided? Let Grandma's Oracle remind you of a dish that has been neglected for over 30 days!")
    
    # 1. Prominent Random Suggestion Button
    if st.button("Remind Me of a Forgotten Gem ✨", type="primary", use_container_width=True):
        forgotten_recipes = db.get_forgotten_recipes()
        all_recipes = db.get_all_recipes()
        
        if not all_recipes:
            st.session_state.suggested_recipe = "empty_db"
        elif not forgotten_recipes:
            st.session_state.suggested_recipe = "none_forgotten"
        else:
            st.session_state.suggested_recipe = random.choice(forgotten_recipes)
            
    # Handle suggested recipe state display
    suggested = st.session_state.suggested_recipe
    
    if suggested == "empty_db":
        st.markdown("""
            <div class="fallback-box" style="background: rgba(231, 111, 81, 0.05); border-color: rgba(231, 111, 81, 0.3);">
                <span style="font-size: 2.5rem;">🍲</span>
                <div class="fallback-title" style="color: #E76F51;">Your Recipe Vault is Empty</div>
                <p class="fallback-text">Please go to the <b>Add New Recipe 📝</b> tab to log your household's special dishes!</p>
            </div>
        """, unsafe_allow_html=True)
        
    elif suggested == "none_forgotten":
        st.markdown("""
            <div class="fallback-box">
                <span style="font-size: 2.5rem;">🎉</span>
                <div class="fallback-title">All your recipes are fresh in memory!</div>
                <p class="fallback-text">You have cooked all your preserved recipes within the last 30 days. You're doing amazing! ❤️</p>
            </div>
        """, unsafe_allow_html=True)
        
    elif isinstance(suggested, dict):
        # We need to make sure the suggested recipe still exists in the DB
        recipes = db.get_all_recipes()
        current_recipe = next((r for r in recipes if r['id'] == suggested['id']), None)
        
        if not current_recipe:
            st.session_state.suggested_recipe = None
            st.rerun()
            
        # Parse ingredients
        ing_list = [i.strip() for i in current_recipe['ingredients'].split(',')]
        ing_html = "".join([f'<span class="ingredient-tag">{i}</span>' for i in ing_list])
        
        st.markdown(f"""
            <div class="gem-card">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1rem;">
                    <span class="badge badge-forgotten">⏳ Forgotten {current_recipe['days_since_cooked']} days</span>
                    <span style="font-size: 0.85rem; color: #5C6B73; font-weight: 600;">{current_recipe['region']} • {current_recipe['category']}</span>
                </div>
                <h3 style="font-size: 2.2rem; color: #E76F51; margin-top: 0; margin-bottom: 0.5rem; font-weight: 800;">{current_recipe['name']}</h3>
                <p style="font-style: italic; color: #4A4A4A; margin-bottom: 1.25rem; font-size: 1rem; border-left: 3px solid #E76F51; padding-left: 10px;">
                    "{current_recipe['notes'] or 'No family secrets added yet.'}"
                </p>
                <h4 style="font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #D95D39; margin-bottom: 0.5rem;">Ingredients Needed:</h4>
                <div style="margin-bottom: 1.25rem;">
                    {ing_html}
                </div>
                <h4 style="font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; color: #D95D39; margin-bottom: 0.5rem;">Preparation Steps:</h4>
                <p style="color: #2F3E46; font-size: 0.95rem; line-height: 1.5; margin-bottom: 1.25rem;">
                    {current_recipe['procedure']}
                </p>
                <div style="font-size: 0.8rem; color: #6D7A80;">
                    Last prepared on: {current_recipe['last_cooked_date']}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Action Buttons
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("I Cooked This Today! 🍳", type="secondary", use_container_width=True):
                db.mark_as_cooked_today(current_recipe['id'])
                st.toast(f"Hooray! Marked '{current_recipe['name']}' as cooked today! 🍽️")
                st.balloons()
                st.session_state.suggested_recipe = None
                st.rerun()
        with col_btn2:
            if st.button("Roll Another Gem 🔄", type="secondary", use_container_width=True):
                forgotten_recipes = db.get_forgotten_recipes()
                # filter out current suggestion if multiple exist
                other_forgotten = [r for r in forgotten_recipes if r['id'] != current_recipe['id']]
                if other_forgotten:
                    st.session_state.suggested_recipe = random.choice(other_forgotten)
                elif forgotten_recipes:
                    st.session_state.suggested_recipe = random.choice(forgotten_recipes)
                else:
                    st.session_state.suggested_recipe = "none_forgotten"
                st.rerun()

# ====================
# TAB 2: RECIPE VAULT 🗂️
# ====================
with tab2:
    st.markdown("### 🗂️ Preserved Recipe Vault")
    st.write("Browse your full collection of traditional recipes, search ingredients, or filter by Type of Dish.")
    
    # Search and Category Filters
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        search_q = st.text_input("🔍 Search recipes or ingredients...", "", placeholder="e.g. Masala, Rice, Garlic...", key="vault_search")
    with f_col2:
        category_filter = st.selectbox("Type of Dish Filter", ["All", "Main Course", "Curry", "Starters", "Breakfast", "Dessert", "Snack", "Bread", "Side Dish", "Other"], key="vault_category_filter")
    
    all_recipes_list = db.get_all_recipes()
    
    if not all_recipes_list:
        st.info("No recipes saved yet. Click the 'Add New Recipe' tab to begin.")
    else:
        # Filter logic
        filtered_list = []
        for r in all_recipes_list:
            if search_q:
                q = search_q.lower()
                if q not in r['name'].lower() and q not in r['ingredients'].lower():
                    continue
            if category_filter != "All" and r['category'] != category_filter:
                continue
            filtered_list.append(r)
            
        st.markdown(f"**Showing {len(filtered_list)} recipes**")
        
        # Display as cards
        for r in filtered_list:
            # Inline edit block check
            if st.session_state.editing_recipe_id == r['id']:
                st.markdown(f"#### ✏️ Edit Recipe: **{r['name']}**")
                with st.form(key=f"edit_form_{r['id']}"):
                    st.markdown("<h4 class='form-section-header'>📋 Edit Recipe Details</h4>", unsafe_allow_html=True)
                    edit_name = st.text_input("Recipe Name*", value=r['name'])
                    edit_category = st.selectbox("Type of Dish (Compulsory)*", ["Select Type...", "Main Course", "Curry", "Starters", "Breakfast", "Dessert", "Snack", "Bread", "Side Dish", "Other"], index=["Select Type...", "Main Course", "Curry", "Starters", "Breakfast", "Dessert", "Snack", "Bread", "Side Dish", "Other"].index(r['category']) if r['category'] in ["Select Type...", "Main Course", "Curry", "Starters", "Breakfast", "Dessert", "Snack", "Bread", "Side Dish", "Other"] else 0)
                    
                    st.markdown("<h4 class='form-section-header'>🍳 Ingredients & Cooking Method</h4>", unsafe_allow_html=True)
                    edit_ingredients = st.text_area("Ingredients Needed (comma-separated)*", value=r['ingredients'])
                    edit_procedure = st.text_area("Preparation Steps / Procedure*", value=r['procedure'])
                    
                    st.markdown("<h4 class='form-section-header'>🗓️ Preparation History</h4>", unsafe_allow_html=True)
                    edit_date = st.date_input("Last Cooked Date", value=datetime.date.fromisoformat(r['last_cooked_date']), max_value=datetime.date.today())
                    
                    with st.expander("Additional Notes (Optional)"):
                        edit_region = st.selectbox("Region", ["Pan-India", "North India", "South India", "East India", "West India", "Other"], index=["Pan-India", "North India", "South India", "East India", "West India", "Other"].index(r['region']) if r['region'] in ["Pan-India", "North India", "South India", "East India", "West India", "Other"] else 0)
                        edit_notes = st.text_area("Family Secrets & Tips (Notes)", value=r['notes'])
                        
                    col_edit_s1, col_edit_s2 = st.columns(2)
                    with col_edit_s1:
                        if st.form_submit_button("Save Changes", use_container_width=True):
                            if not edit_name:
                                st.error("Recipe Name is required.")
                            elif edit_category == "Select Type...":
                                st.error("Please select a Type of Dish.")
                            elif not edit_ingredients:
                                st.error("Ingredients are required.")
                            elif not edit_procedure:
                                st.error("Preparation Steps/Procedure is required.")
                            else:
                                db.update_recipe(
                                    r['id'],
                                    edit_name,
                                    edit_ingredients,
                                    edit_category,
                                    edit_region,
                                    edit_date.isoformat(),
                                    edit_notes,
                                    edit_procedure
                                )
                                st.toast(f"Updated '{edit_name}' successfully!")
                                st.session_state.editing_recipe_id = None
                                st.session_state.suggested_recipe = None
                                st.rerun()
                    with col_edit_s2:
                        if st.form_submit_button("Cancel", use_container_width=True):
                            st.session_state.editing_recipe_id = None
                            st.rerun()
                st.markdown("---")
            else:
                # Normal Display Card
                badge_type = "badge-forgotten" if r['status'] == "Forgotten" else ("badge-nearing" if r['status'] == "Nearing Forgotten" else "badge-active")
                
                # Split ingredients
                i_list = [i.strip() for i in r['ingredients'].split(',')]
                i_html = "".join([f'<span class="ingredient-tag">{i}</span>' for i in i_list])
                
                st.markdown(f"""
                    <div class="recipe-card">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span class="badge {badge_type}">{r['status']} ({r['days_since_cooked']}d ago)</span>
                            <span style="font-size: 0.8rem; color: #6D7A80;">{r['region']} • {r['category']}</span>
                        </div>
                        <h4 style="font-size: 1.4rem; color: #2F3E46; margin: 0 0 0.5rem 0; font-weight: 700;">{r['name']}</h4>
                        <div style="margin-bottom: 0.75rem;">{i_html}</div>
                        <div style="margin-bottom: 0.75rem; font-size: 0.9rem; color: #2F3E46; line-height: 1.4;">
                            <b>Steps:</b> {r['procedure']}
                        </div>
                        {f'<p style="font-size: 0.85rem; color: #5C6B73; font-style: italic; margin-bottom: 0.5rem;">Notes: "{r["notes"]}"</p>' if r['notes'] else ''}
                    </div>
                """, unsafe_allow_html=True)
                
                # Actions for each card
                col_act1, col_act2, col_act3 = st.columns([2, 1, 1])
                with col_act1:
                    if st.button("Cooked Today 🍳", key=f"cook_va_{r['id']}", type="secondary", use_container_width=True):
                        db.mark_as_cooked_today(r['id'])
                        st.toast(f"Cooked '{r['name']}' today! 🍽️")
                        st.session_state.suggested_recipe = None
                        st.rerun()
                with col_act2:
                    if st.button("✏️", key=f"edit_va_{r['id']}", use_container_width=True, help="Edit Recipe"):
                        st.session_state.editing_recipe_id = r['id']
                        st.rerun()
                with col_act3:
                    if st.button("🗑️", key=f"del_va_{r['id']}", use_container_width=True, help="Delete Recipe"):
                        st.session_state[f"confirm_del_{r['id']}"] = True
                        st.rerun()
                        
                if st.session_state.get(f"confirm_del_{r['id']}", False):
                    st.markdown(f"<div style='padding: 0.75rem; border: 1px solid rgba(231,111,81,0.3); border-radius:8px; background:rgba(231,111,81,0.02); margin-bottom: 1rem;'><small style='color:#E76F51; font-weight:bold;'>Delete '{r['name']}' permanently?</small></div>", unsafe_allow_html=True)
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Delete ✅", key=f"yes_del_{r['id']}", use_container_width=True):
                            db.delete_recipe(r['id'])
                            st.toast(f"Deleted '{r['name']}'")
                            st.session_state[f"confirm_del_{r['id']}"] = False
                            st.session_state.suggested_recipe = None
                            st.rerun()
                    with c2:
                        if st.button("Cancel ❌", key=f"no_del_{r['id']}", use_container_width=True):
                            st.session_state[f"confirm_del_{r['id']}"] = False
                            st.rerun()

# ====================
# TAB 3: ADD NEW RECIPE 📝 (Upgraded with AI Smart Input)
# ====================
with tab3:
    st.markdown("### 📝 Preserve a Recipe")
    st.write("Preserve family traditions, recipes, and notes to pass them down and keep them in kitchen rotation!")
    
    # AI Smart Hub Section
    st.markdown("<h4 class='form-section-header'>🪄 AI Fast-Fill Helper (Optional)</h4>", unsafe_allow_html=True)
    st.write("Avoid typing entirely! Snap a photo of a handwritten card or simply record voice dictation in your natural household language.")
    
    ai_mode = st.radio("Choose AI Input Method:", ["❌ Don't use AI", "📸 Upload Recipe Photo", "🎙️ Record Voice Command"])
    
    ai_data = None
    ai_mime = None
    
    if ai_mode == "📸 Upload Recipe Photo":
        uploaded_img = st.file_uploader("Upload a screenshot or photo of handwritten cooking notes", type=["jpg", "jpeg", "png"])
        if uploaded_img:
            ai_data = uploaded_img.getvalue()
            ai_mime = uploaded_img.type
            st.image(uploaded_img, caption="Loaded Image File", width=250)
            
    elif ai_mode == "🎙️ Record Voice Command":
        st.write("Click record and casually dictate details like recipe name, elements, steps, and tips out loud:")
        audio_clip = mic_recorder(start_prompt="🎙️ Start Recording", stop_prompt="⏹️ Stop Recording", key='tab3_recorder')
        if audio_clip:
            ai_data = audio_clip['bytes']
            ai_mime = "audio/wav"
            st.audio(ai_data, format="audio/wav")

    # Run AI analysis if data was supplied
    if ai_data and client:
        if st.button("✨ Auto-Fill Form via AI", type="secondary", use_container_width=True):
            with st.spinner("🧠 Unscrambling language context and organizing fields..."):
                try:
                    prompt_structure = """
                    You are an Indian kitchen archivist reading recipe notes or voice transmissions.
                    Analyze the data which might contain structural mixtures of English and Indian dialect terminology (Hinglish, kitchen slang, etc.).
                    Extract info and return exactly 5 parts separated strictly by '---'. No extra conversational filler.
                    
                    PART 1 (NAME): Short concise recipe title in English script.
                    ---
                    PART 2 (CATEGORY): Choose exactly one matching option from: Main Course, Curry, Starters, Breakfast, Dessert, Snack, Bread, Side Dish, Other.
                    ---
                    PART 3 (INGREDIENTS): Extract ingredients as a simple comma-separated string on a single line (e.g. Rice, Milk, Sugar, Cardamom). Do not use bullet points or dashes.
                    ---
                    PART 4 (PROCEDURE): Step-by-step instructions. Clear and numbered cleanly.
                    ---
                    PART 5 (NOTES): Family secrets, tips, or regional observations.
                    """
                    
                    ai_response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[{"inline_data": {"data": ai_data, "mime_type": ai_mime}}, prompt_structure]
                    )
                    
                    parsed_parts = ai_response.text.split("---")
                    if len(parsed_parts) >= 5:
                        st.session_state["prefilled_name"] = parsed_parts[0].replace("PART 1 (NAME):", "").strip()
                        st.session_state["prefilled_category"] = parsed_parts[1].replace("PART 2 (CATEGORY):", "").strip()
                        st.session_state["prefilled_ingredients"] = parsed_parts[2].replace("PART 3 (INGREDIENTS):", "").strip()
                        st.session_state["prefilled_procedure"] = parsed_parts[3].replace("PART 4 (PROCEDURE):", "").strip()
                        st.session_state["prefilled_notes"] = parsed_parts[4].replace("PART 5 (NOTES):", "").strip()
                        st.success("Form updated! Review the details in the form below before finalizing saving.")
                    else:
                        st.error("AI output parser failed format checking. Please write manually or re-record cleanly.")
                except Exception as ex:
                    st.error(f"AI parsing module error: {ex}")

    # Set up form variable defaults derived from standard tracking or session tracking configurations
    init_name = st.session_state.get("prefilled_name", "")
    init_ingredients = st.session_state.get("prefilled_ingredients", "")
    init_procedure = st.session_state.get("prefilled_procedure", "")
    init_notes = st.session_state.get("prefilled_notes", "")
    
    category_options = ["Select Type...", "Main Course", "Curry", "Starters", "Breakfast", "Dessert", "Snack", "Bread", "Side Dish", "Other"]
    ai_cat_choice = st.session_state.get("prefilled_category", "Select Type...")
    init_cat_idx = category_options.index(ai_cat_choice) if ai_cat_choice in category_options else 0

    # Primary Entry Form
    with st.form(key="add_recipe_form", clear_on_submit=True):
        st.markdown("<h4 class='form-section-header'>📋 Recipe Details</h4>", unsafe_allow_html=True)
        new_name = st.text_input("Recipe Name*", value=init_name, placeholder="e.g. Dadi's Special Kheer")
        new_category = st.selectbox("Type of Dish (Compulsory)*", options=category_options, index=init_cat_idx)
        
        st.markdown("<h4 class='form-section-header'>🍳 Ingredients & Cooking Method</h4>", unsafe_allow_html=True)
        new_ingredients = st.text_area("Ingredients Needed (comma-separated)*", value=init_ingredients, placeholder="e.g. Rice, Milk, Sugar, Saffron, Almonds")
        new_procedure = st.text_area("Preparation Steps / Procedure*", value=init_procedure, placeholder="e.g. 1. Wash rice. 2. Boil milk and add rice. 3. Simmer until rice is cooked. 4. Add sugar and garnish with nuts.")
        
        st.markdown("<h4 class='form-section-header'>🗓️ Preparation History</h4>", unsafe_allow_html=True)
        new_date = st.date_input("Last Cooked Date", value=datetime.date.today(), max_value=datetime.date.today())
        
        with st.expander("Additional Notes (Optional)"):
            new_region = st.selectbox("Region", ["Pan-India", "North India", "South India", "East India", "West India", "Other"])
            new_notes = st.text_area("Family Secrets & Tips (Notes)", value=init_notes, placeholder="E.g. Serve chilled for best taste...")
            
        submit_btn = st.form_submit_button("Save Recipe", use_container_width=True)
        
        if submit_btn:
            if not new_name:
                st.error("Recipe Name is required.")
            elif new_category == "Select Type...":
                st.error("Please select a Type of Dish.")
            elif not new_ingredients:
                st.error("Ingredients list is required.")
            elif not new_procedure:
                st.error("Preparation Steps/Procedure is required.")
            else:
                db.add_recipe(
                    new_name,
                    new_ingredients,
                    new_category,
                    new_region,
                    new_date.isoformat(),
                    new_notes,
                    new_procedure
                )
                st.toast(f"🎉 Saved '{new_name}' to Vault!")
                st.session_state.suggested_recipe = None  # Clear suggestion state to force refresh
                
                # Clear prefill cache keys out cleanly upon completion
                for k in ["prefilled_name", "prefilled_category", "prefilled_ingredients", "prefilled_procedure", "prefilled_notes"]:
                    if k in st.session_state:
                        del st.session_state[k]
                        
                st.success(f"Successfully saved '{new_name}' to the Recipe Vault!")
                st.rerun()
