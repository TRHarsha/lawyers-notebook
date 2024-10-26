import os
import pandas as pd
import streamlit as st

# Define the path for the cases CSV file
cases_file = "cases.csv"  # Adjust the file path as necessary

def load_cases():
    if os.path.exists(cases_file):
        try:
            df = pd.read_csv(cases_file)
            if df.empty:
                st.warning("The cases file is empty.")
                return pd.DataFrame(columns=['Case ID', 'Case Title', 'Client', 'Status', 'Date'])
            return df
        except pd.errors.EmptyDataError:
            st.warning("The cases file is empty.")
            return pd.DataFrame(columns=['Case ID', 'Case Title', 'Client', 'Status', 'Date'])
        except Exception as e:
            st.error(f"An error occurred while loading cases: {e}")
            return pd.DataFrame(columns=['Case ID', 'Case Title', 'Client', 'Status', 'Date'])
    else:
        st.warning("Cases file does not exist. Creating a new one.")
        return pd.DataFrame(columns=['Case ID', 'Case Title', 'Client', 'Status', 'Date'])

# Main application code
if __name__ == "__main__":
    st.title("Lawyer's Notes App")

    # Display all cases
    st.subheader("Your Cases")
    cases_df = load_cases()  # Call the load_cases function
    if not cases_df.empty:
        st.write(cases_df)
    else:
        st.write("No cases to display.")
