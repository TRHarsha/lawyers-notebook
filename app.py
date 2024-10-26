import os
import pandas as pd
import streamlit as st

def load_notes():
    if os.path.exists(notes_file):
        try:
            df = pd.read_csv(notes_file)
            if df.empty:
                st.warning("The notes file is empty.")
                return pd.DataFrame(columns=['Note ID', 'Case ID', 'Content', 'Date'])
            return df
        except pd.errors.EmptyDataError:
            st.warning("The notes file is empty.")
            return pd.DataFrame(columns=['Note ID', 'Case ID', 'Content', 'Date'])
        except Exception as e:
            st.error(f"An error occurred while loading notes: {e}")
            return pd.DataFrame(columns=['Note ID', 'Case ID', 'Content', 'Date'])
    else:
        st.warning("Notes file does not exist. Creating a new one.")
        return pd.DataFrame(columns=['Note ID', 'Case ID', 'Content', 'Date'])


# Function to save a case to the CSV file
def save_case(case_id, client_name, case_desc, deadline):
    df = load_cases()
    new_case = {'Case ID': case_id, 'Client Name': client_name, 'Case Description': case_desc, 'Deadline': deadline}
    df = df.append(new_case, ignore_index=True)
    df.to_csv(cases_file, index=False)

# Function to load notes from the CSV file
def load_notes():
    if os.path.exists(notes_file):
        return pd.read_csv(notes_file)
    else:
        return pd.DataFrame(columns=['Note', 'Timestamp'])

# Function to save a note to the CSV file
def save_note(note):
    df = load_notes()
    new_note = {'Note': note, 'Timestamp': pd.Timestamp.now()}
    df = df.append(new_note, ignore_index=True)
    df.to_csv(notes_file, index=False)

# Streamlit application
st.title("Lawyer Dashboard")

# Case Management Section
st.header("Case Management")
with st.form(key='case_form'):
    case_id = st.text_input("Case ID")
    client_name = st.text_input("Client Name")
    case_desc = st.text_area("Case Description")
    deadline = st.date_input("Deadline")
    submit_case = st.form_submit_button("Add Case")

    if submit_case:
        if case_id and client_name and case_desc and deadline:
            save_case(case_id, client_name, case_desc, deadline)
            st.success("Case added successfully!")
        else:
            st.warning("Please fill all fields.")

# Display all cases
st.subheader("Your Cases")
cases_df = load_cases()
if not cases_df.empty:
    st.write(cases_df)
else:
    st.write("No cases available.")

# Notes Section
st.header("Notes")
note_input = st.text_area("Add your note here:")
if st.button("Save Note"):
    if note_input:
        save_note(note_input)
        st.success("Note saved successfully!")
    else:
        st.warning("Please enter a note.")

# Load and display notes
notes_df = load_notes()
st.subheader("Your Notes")
if not notes_df.empty:
    for index, row in notes_df.iterrows():
        st.write(f"{row['Timestamp']}: {row['Note']}")
else:
    st.write("No notes available.")

# Statistics Section
st.header("Statistics")
st.write(f"Total Cases: {len(cases_df)}")
st.write(f"Total Notes: {len(notes_df)}")
