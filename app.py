import streamlit as st
import pandas as pd

# Load trait descriptions
@st.cache_data
def load_data():
    file_path = "Trait_Descriptions_by_State.xlsx"
    df = pd.read_excel(file_path)
    return df

# Score-to-state mapping
behavior_mapping = {1: "Less Active", 2: "Less Active", 3: "Balanced", 4: "Active", 5: "Active"}
personality_psyche_mapping = {
    1: "Less Active", 2: "Less Active", 3: "Less Active",
    4: "Balanced", 5: "Active", 6: "Active", 7: "Active"
}

def get_state(level, score):
    if level == "Behaviour":
        return behavior_mapping.get(score, "Invalid Score")
    else:
        return personality_psyche_mapping.get(score, "Invalid Score")

def main():
    st.title("Trait Feedback Generator")
    df = load_data()
    traits = df["Trait"].unique()
    trait_levels = df.drop_duplicates("Trait")[["Trait", "Level"]].set_index("Trait").to_dict()["Level"]

    st.write("### Please enter your scores:")
    scores = {}
    for trait in traits:
        level = trait_levels[trait]
        max_score = 5 if level == "Behaviour" else 7
        score = st.slider(f"{trait} ({level})", 1, max_score, 3)
        scores[trait] = score

    if st.button("Generate Feedback"):
        feedback = []
        for trait, score in scores.items():
            level = trait_levels[trait]
            state = get_state(level, score)
            desc_row = df[(df["Trait"] == trait) & (df["State"] == state)]
            if not desc_row.empty:
                description = desc_row["Description"].values[0]
            else:
                description = "No description available."
            feedback.append({
                "Trait": trait,
                "Level": level,
                "Score": score,
                "Mapped State": state,
                "Description": description
            })

        result_df = pd.DataFrame(feedback)
        st.write("### Feedback Summary")
        st.dataframe(result_df)

        # Offer to download
        st.download_button(
            label="Download Feedback as CSV",
            data=result_df.to_csv(index=False),
            file_name="trait_feedback.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
