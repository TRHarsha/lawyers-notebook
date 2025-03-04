import streamlit as st
import pandas as pd
import os

# Define file paths for cases and notes
cases_file = 'lawyer_cases.csv'
notes_file = 'lawyer_notes.csv'

# Function to load data from CSV files
def load_data(file_path, columns):
    if os.path.exists(file_path):
        try:
            if os.path.getsize(file_path) == 0:
                df = pd.DataFrame(columns=columns)
                df.to_csv(file_path, index=False)
                return df
            return pd.read_csv(file_path, encoding="utf-8", usecols=columns)
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=columns)
    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df

# Function to save data to CSV files
def save_data(file_path, data):
    df = load_data(file_path, data.columns)
    df = pd.concat([df, data], ignore_index=True)
    df.to_csv(file_path, index=False)

# Streamlit application
st.title("Lawyer Notebook")

# Case Management Section
st.header("Case Management")
with st.form(key='case_form'):
    case_id = st.text_input("Case ID")
    client_name = st.text_input("Client Name")
    case_desc = st.text_area("Case Description")
    status = st.selectbox("Status", ["Open", "In Progress", "Closed"])
    submit_case = st.form_submit_button("Add Case")

    if submit_case:
        if case_id and client_name and case_desc and status:
            new_case = pd.DataFrame({
                'Case ID': [case_id],
                'Client Name': [client_name],
                'Case Description': [case_desc],
                'Status': [status]
            })
            save_data(cases_file, new_case)
            st.success("Case added successfully!")
            st.experimental_rerun()
        else:
            st.warning("Please fill all fields.")

# Display all cases
st.subheader("Your Cases")
cases_df = load_data(cases_file, ['Case ID', 'Client Name', 'Case Description', 'Status'])
if not cases_df.empty:
    st.write(cases_df)
else:
    st.write("No cases available.")

# Notes Section
st.header("Notes")
note_input = st.text_area("Add your note here:")
if st.button("Save Note"):
    if note_input:
        new_note = pd.DataFrame({
            'Note': [note_input],
            'Timestamp': [pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")]
        })
        save_data(notes_file, new_note)
        st.success("Note saved successfully!")
        st.experimental_rerun()
    else:
        st.warning("Please enter a note.")

# Load and display notes
st.subheader("Your Notes")
notes_df = load_data(notes_file, ['Note', 'Timestamp'])
if not notes_df.empty:
    for index, row in notes_df.iterrows():
        st.write(f"{row['Timestamp']}: {row['Note']}")
else:
    st.write("No notes available.")

# Statistics Section
st.header("Statistics")
st.write(f"Total Cases: {len(cases_df)}")
st.write(f"Total Notes: {len(notes_df)}")
