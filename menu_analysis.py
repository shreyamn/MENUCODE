import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# ---------- Constants ----------
STARTERS = ['🥗 Salad', '🍲 Soup', '🍞 Bruschetta', '🧄 Garlic Bread', '🌮 Nachos']
MAINS = ['🍛 Paneer Curry', '🍚 Veg Biryani', '🍝 Pasta', '🍕 Pizza', '🍔 Burger']
DESSERTS = ['🍰 Cheesecake', '🍫 Brownie', '🍦 Ice Cream', '🍮 Gulab Jamun', '🍓 Fruit Salad']
DATA_FILE = 'menu_ratings.csv'
CHEF_PASSWORD = "chef123"

# ---------- Helper Functions ----------
def init_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=['email', 'course', 'item', 'rating'])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_rating(email, course, item, rating):
    df = load_data()
    new_entry = {'email': email, 'course': course, 'item': item, 'rating': rating}
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

def visualize_data():
    df = load_data()
    st.markdown("### 📊 Ratings Visualization")

    for course, items in {'Starters': STARTERS, 'Main Course': MAINS, 'Desserts': DESSERTS}.items():
        st.markdown(f"#### 🍽️ {course}")
        course_df = df[df['course'] == course]
        if not course_df.empty:
            chart_data = course_df.groupby('item')['rating'].mean()
            fig, ax = plt.subplots()
            ax.pie(chart_data, labels=chart_data.index, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.info(f"No ratings yet for **{course}**.")

# ---------- Main App ----------
st.set_page_config("🍽️ Menu Analysis App", layout="centered")
st.markdown("# 🍽️ Menu Analysis App")
st.markdown("Welcome! Rate your favorite dishes or view ratings as a chef.")

init_data()

role = st.radio("👤 Select your role:", ["Customer", "Chef"])

if role == "Customer":
    st.markdown("## 🧍 Please register by entering your email address")
    email = st.text_input("📧 Enter your Gmail")

    if email and email.endswith("@gmail.com"):
        st.success("Welcome! Scroll down to rate the menu items.")

        for course, items in {'Starters': STARTERS, 'Main Course': MAINS, 'Desserts': DESSERTS}.items():
            st.markdown(f"### 🍽️ {course}")
            for item in items:
                rating = st.slider(f"⭐ Rate {item}", 1, 5, 3, key=f"{course}_{item}")
                if st.button(f"✅ Submit Rating for {item}", key=f"btn_{course}_{item}"):
                    save_rating(email, course, item, rating)
                    st.success(f"Thank you! Your rating for {item} is saved.")
    elif email:
        st.error("❌ Please enter a valid Gmail address (ends with @gmail.com)")

elif role == "Chef":
    st.markdown("## 👨‍🍳 Chef Login")
    password = st.text_input("🔑 Enter Chef Password", type="password")
    if password == CHEF_PASSWORD:
        st.success("Access granted! View real-time ratings below.")
        visualize_data()
    elif password:
        st.error("❌ Incorrect password.")
