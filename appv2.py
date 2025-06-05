import streamlit as st
import pandas as pd

# --- Dummy credentials for login ---
USER_CREDENTIALS = {
    "admin": "password123",
    "user": "letmein"
}

# --- Login function ---
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        st.stop()

# --- Call login function ---
login()

# --- Main App Content ---
st.title("Trait Feedback Entry Tool")

st.markdown("""
Enter your trait ratings below. 

- Behaviour traits: 1 (Not Active) to 5 (Very Active)
- Personality and Psyche traits: 1 (Inactive) to 7 (Very Active)
""")

# Load trait structure from file
file_path = "Trait_Descriptions_by_State_Template.xlsx"
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error(f"Excel file not found: {file_path}")
    st.stop()

categories = df['Category'].unique()
input_scores = {}

for cat in categories:
    st.subheader(cat)
    traits = df[df['Category'] == cat]['Trait'].unique()
    for trait in traits:
        if cat == "Behaviour":
            score = st.slider(trait, 1, 5, 3)
        else:
            score = st.slider(trait, 1, 7, 4)
        input_scores[trait] = score

# Save or process inputs
if st.button("Submit"):
    result_df = pd.DataFrame(list(input_scores.items()), columns=["Trait", "Score"])
    st.success("Trait feedback submitted successfully!")
    st.dataframe(result_df)
    result_df.to_excel("submitted_trait_scores.xlsx", index=False)
    st.download_button("Download Submitted Scores", data=result_df.to_csv(index=False), file_name="trait_scores.csv", mime="text/csv")
