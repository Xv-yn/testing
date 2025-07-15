import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import datetime

# Starter tactic library (expandable)
TACTIC_LIBRARY = [
    # Awareness Stage (example; add more up to 350)
    {"name": "Social Media Teasers", "stage": "Awareness", "description": "Post short videos on Instagram/TikTok."},
    {"name": "Influencer Partnerships", "stage": "Awareness", "description": "Collaborate with K-beauty influencers."},
    # Add more tactics here...
    # Consideration, Conversion, Loyalty similarly
]

# Load data from CSV (persistent via GitHub)
DATA_FILE = 'miist_aura_campaigns.csv'
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=['Campaign Name', 'Funnel Stage', 'Tactics', 'Status', 'Budget', 'ROI', 'Start Date', 'End Date', 'Notes'])

def save_data():
    df.to_csv(DATA_FILE, index=False)
# Simple strategy generator
def generate_strategy(campaign_name, funnel_stage):
    tactics = [t['name'] for t in TACTIC_LIBRARY if t['stage'] == funnel_stage]
    if tactics:
        return f"Strategy for '{campaign_name}': Use {', '.join(tactics[:5])}. Track weekly."
    return "No tactics for this stage."

# Streamlit App
st.title("Miist Aura Campaign Tracker")

# Sidebar Menu
menu = st.sidebar.selectbox("Menu", ["Add Campaign", "View/Update Campaigns", "Generate Strategy", "View Tactic Library", "Reports"])

if menu == "Add Campaign":
    with st.form("Add Campaign Form"):
        name = st.text_input("Campaign Name")
        stage = st.selectbox("Funnel Stage", ["Awareness", "Consideration", "Conversion", "Loyalty"])
        tactics = st.text_input("Assigned Tactics (comma-separated)")
        status = st.selectbox("Status", ["Planned", "In Progress", "Completed"])
        budget = st.number_input("Budget", min_value=0.0)
        roi = st.number_input("ROI (estimated)", min_value=0.0)
        start = datetime.date.today()
        end = st.date_input("End Date")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add")
        if submitted:
            new_row = pd.DataFrame([[name, stage, tactics, status, budget, roi, start, end, notes]], columns=df.columns)
            global df
            df = pd.concat([df, new_row], ignore_index=True)
            save_data()
            st.success("Campaign added!")

elif menu == "View/Update Campaigns":
    st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("Save Changes"):
        save_data()
        st.success("Saved!")

elif menu == "Generate Strategy":
    name = st.text_input("Campaign Name")
    stage = st.selectbox("Funnel Stage", ["Awareness", "Consideration", "Conversion", "Loyalty"])
    if st.button("Generate"):
        st.write(generate_strategy(name, stage))

elif menu == "View Tactic Library":
    for t in TACTIC_LIBRARY:
        st.write(f"{t['name']} ({t['stage']}): {t['description']}")

elif menu == "Reports":
    st.write(df.describe())
    fig, ax = plt.subplots()
    df['Funnel Stage'].value_counts().plot(kind='bar', ax=ax)
    st.pyplot(fig)
    st.download_button("Export CSV", df.to_csv(index=False), "campaigns.csv")