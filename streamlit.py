import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path, header=None, names=['review'])

def save_progress(data, file_path):
    data.to_csv(file_path, index=False)

# Path to the uploaded file
file_path = 'rs_moewardi.csv'

# Initialize state
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'labeled_data' not in st.session_state:
    st.session_state.labeled_data = load_data(file_path)
    st.session_state.labeled_data['Label'] = ''

# Save progress automatically
save_progress(st.session_state.labeled_data, 'progress.csv')

# Display current progress
st.title("Sentiment Labeling App")
st.write(f"Progress: {st.session_state.current_index + 1}/{len(st.session_state.labeled_data)}")

# Display current review
try:
    current_review = st.session_state.labeled_data.iloc[st.session_state.current_index]
    st.write(current_review['review'])
except KeyError:
    st.error("Error accessing the review. Please check the dataset format.")
    st.stop()

# Labeling buttons
if st.button('Positif'):
    st.session_state.labeled_data.at[st.session_state.current_index, 'Label'] = 'Positif'
    st.session_state.current_index += 1
if st.button('Negatif'):
    st.session_state.labeled_data.at[st.session_state.current_index, 'Label'] = 'Negatif'
    st.session_state.current_index += 1
if st.button('Netral'):
    st.session_state.labeled_data.at[st.session_state.current_index, 'Label'] = 'Netral'
    st.session_state.current_index += 1

# Previous button
if st.button('Previous'):
    st.session_state.current_index = max(0, st.session_state.current_index - 1)

# Check if finished
if st.session_state.current_index >= len(st.session_state.labeled_data):
    st.write("Labeling finished! Saving final labeled dataset...")
    save_progress(st.session_state.labeled_data, 'labeled_dataset.csv')
    st.stop()

# Save progress after each change
save_progress(st.session_state.labeled_data, 'progress.csv')
