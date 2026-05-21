# Implementation Plan (Updated) - Recipe Reminder App

We will modify the application layout to support exactly **three tabs**, separating the random suggestion feature from the recipe browsing directory, and introducing detailed "Type of Dish" filtering in the directory.

## Proposed Layout Changes

### Tab 1: "🥗 What to Cook Today" (Homepage)
- **Content**: 
  - Prominent "Remind Me of a Forgotten Gem ✨" button.
  - The suggested recipe card display with its action buttons ("I Cooked This Today! 🍳" and "Roll Another Gem 🔄").
  - The fallback/empty states.
- **Removed**: The full recipe list/directory and search bar will be completely removed from this screen to keep the homepage clutter-free.

### Tab 2: "🗂️ Recipe Vault"
- **Content**: 
  - A clean search and filter bar at the top.
  - **Type of Dish Filter**: A selectbox or row of buttons/pills to filter recipes by Type of Dish (e.g., Main Course, Curry, Starters, Breakfast, Dessert, Snack, etc.).
  - The complete list of saved recipes displayed as cards.
  - Actions for each card: "Cooked Today 🍳", inline editing, and deletion (with confirmation).

### Tab 3: "Add New Recipe 📝"
- **Content**: The recipe creation form with clear headings and validation constraints.

---

## Verification Plan

1. **Tab Structure**:
   - Verify the presence of exactly three tabs: `🥗 What to Cook Today`, `🗂️ Recipe Vault`, and `Add New Recipe 📝`.
2. **Filtering by Type of Dish**:
   - Add recipes with various categories (e.g. Starters, Curry, Desserts).
   - Go to Tab 2 and select different "Type of Dish" filter options.
   - Verify that only recipes matching the selected filter are rendered.
3. **Operations**:
   - Check that inline edits and deletes on Tab 2 successfully update the SQLite database and sync immediately with Tab 1's Oracle suggestions.
