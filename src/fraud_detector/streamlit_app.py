# streamlit_app.py
import streamlit as st
from main import run_crew
import os
import tempfile
import pandas as pd

# Set API keys using Streamlit secrets
os.environ["SERPER_API_KEY"] = st.secrets["api_keys"]["SERPER_API_KEY"]
os.environ["OPENAI_API_KEY"] = st.secrets["api_keys"]["OPENAI_API_KEY"]

st.sidebar.title("Upload Transaction Dataset")

uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

st.sidebar.title("Customer Information")

customer_name = st.sidebar.text_input("Customer Name", value="John Doe")
topic = st.sidebar.text_input("Topic", value="Anti-money laundering")

# Dataset description
dataset_description = """
Transaction ID: Unique identifier for each transaction.
Customer ID: Identifier for the customer.
Transaction Timestamp: Date and time of the transaction.
Transaction Amount: Monetary value of the transaction.
Transaction Type: Type of transaction (e.g., deposit, withdrawal, transfer, purchase).
Merchant Category: Business category of the transaction.
Location: Geographic location of the transaction.
Account Balance: Balance before and after the transaction.
Transaction Frequency: Number of transactions made in a short period.
Transaction Partner: Receiver account (e.g., known or anonymous entity).
Country Code: Origin of the transaction.
Transaction Chain: Number of linked transactions (e.g., A → B → C).
"""

st.title("Fraud Detection Crew Chat Interface")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

user_input = st.text_input("Enter your prompt here:")

if st.button("Send") and user_input:
    # Append user message
    st.session_state['messages'].append({"role": "user", "content": user_input})

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    # Prepare customer_info with dataset description
    customer_info = f"The customer transaction history can be accessed using the file at {tmp_file_path}, this is the dataset description: \n{dataset_description}"

    if st.button("Run Fraud Detection Crew"):
        with st.spinner('Processing...'):
            try:
                # Run the crew and get results
                results = run_crew(
                    customer_name=customer_name,
                    customer_info=customer_info,
                    topic=topic,
                    dataset_path=tmp_file_path
                )

                # Append agent response
                if results:
                    # st.session_state['messages'].append({"role": "assistant", "content": str(results)})
                    if hasattr(results, "to_dict"):
                        response_dict = results.to_dict()
                    else:
                        response_dict = vars(results) if isinstance(results, object) else results

                    # Recursive function to flatten nested JSON
                    def flatten_json(data, parent_key=''):
                        items = []
                        for key, value in (data.items() if isinstance(data, dict) else []):
                            new_key = f"{parent_key}.{key}" if parent_key else key
                            if isinstance(value, dict):
                                items.extend(flatten_json(value, new_key).items())
                            elif isinstance(value, list):
                                items.append((new_key, ', '.join(map(str, value))))
                            else:
                                items.append((new_key, value))
                        return dict(items)

                    # Flatten the JSON and display it as a table
                    st.subheader("Answer")
                    flattened_data = flatten_json(response_dict)
                    flattened_df = pd.DataFrame(flattened_data.items(), columns=["Key", "Value"])

                    flattened_df = flattened_df.astype(str)

                    st.table(flattened_df)

            except Exception as e:
                st.error(f"An error occurred: {e}")

# Display the chat messages
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.markdown(f"**You:** {message['content']}")
    else:
        st.markdown(f"**Agent:** {message['content']}")
