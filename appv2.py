import streamlit as st
import pandas as pd

# --- Login system setup ---
users = {
    "admin": "adminpass",
    "maarten": "maarten123",
    "monica": "monica321",
    "judith": "judith321",
    "mireille": "mireille321"
}

def login():
    st.title("🔒 Trait Feedback Tool - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

if "logged_in" not in st.session_state:
    login()
    st.stop()

# --- Main App ---
st.sidebar.success(f"Welcome, {st.session_state['user']}!")

st.title("🧠 Trait Analysis Feedback Tool")

# Load Excel file with descriptions
@st.cache_data

def load_descriptions():
    return pd.read_excel("Trait_Descriptions_by_State.xlsx")

df = load_descriptions()

# Input section
st.header("Enter Scores for Each Trait")

scores = {}

# Separate traits by section
def get_traits(section):
    return df[df["Category"] == section]["Trait"].tolist()

# Score input mapping
score_labels_behavior = {1: "Not Active", 2: "Less Active", 3: "Balanced", 4: "Active", 5: "Very Active"}
score_labels_personality = {1: "Inactive", 2: "Hardly Active", 3: "Less Active", 4: "Balanced", 5: "Slightly Active", 6: "Active", 7: "Very Active"}

st.subheader("Behaviour (1–5)")
for trait in get_traits("Behaviour"):
    score = st.slider(trait, 1, 5, 3)
    scores[trait] = score

st.subheader("Personality (1–7)")
for trait in get_traits("Personality"):
    score = st.slider(trait, 1, 7, 4)
    scores[trait] = score

st.subheader("Psyche (1–7)")
for trait in get_traits("Psyche"):
    score = st.slider(trait, 1, 7, 4)
    scores[trait] = score

# Show feedback descriptions
st.header("📝 Feedback Based on Your Scores")

for trait, score in scores.items():
    category = df[df["Trait"] == trait]["Category"].values[0]
    if category == "Behaviour":
        level = score_labels_behavior[score]
    else:
        level = score_labels_personality[score]

    desc = df[(df["Trait"] == trait) & (df["State"] == level)]["Description"].values
    if len(desc) > 0:
        st.markdown(f"**{trait}** ({level}): {desc[0]}")
    else:
        st.markdown(f"**{trait}** ({level}): _No description available_")
