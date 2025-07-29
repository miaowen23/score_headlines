import streamlit as st
import requests

# Page configuration (must be set at the beginning)
st.set_page_config(page_title="Headline Sentiment Scorer", layout="centered")

st.title("Headline Sentiment Scorer")
st.markdown("Enter your news headlines below. You can add, edit, or remove them before submitting for sentiment analysis.")

API_URL = "http://localhost:8020/score_headlines"

# Debug message to verify the app is running
st.write("Streamlit app is running.")

# Initialize session state to store the list of headlines
if "headlines" not in st.session_state:
    st.session_state.headlines = [""]

# Function to add a new empty input field for headline
def add_headline():
    st.session_state.headlines.append("")

# Function to remove a specific headline input
def remove_headline(index):
    st.session_state.headlines.pop(index)

# Render input fields for each headline
for i, headline in enumerate(st.session_state.headlines):
    cols = st.columns([6, 1])
    st.session_state.headlines[i] = cols[0].text_input(f"Headline {i + 1}", value=headline, key=f"headline_{i}")
    if cols[1].button("Remove", key=f"remove_{i}"):
        remove_headline(i)
        st.experimental_rerun()

# Button to add a new headline input field
st.button("Add Headline", on_click=add_headline)

# Submit button to analyze sentiments via API
if st.button("Analyze Sentiment"):
    input_headlines = [h for h in st.session_state.headlines if h.strip() != ""]
    if not input_headlines:
        st.warning("Please enter at least one headline.")
    else:
        try:
            response = requests.post(API_URL, json={"headlines": input_headlines})
            if response.status_code == 200:
                result = response.json()
                st.subheader("Sentiment Results")
                for headline, label in zip(input_headlines, result["labels"]):
                    st.markdown(f"- **{headline}** → _{label}_")
            else:
                st.error(f"API Error: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to reach API at {API_URL}")
            st.exception(e)
