import sys
from crew import FraudDetectorCrew
import os

os.environ["SERPER_API_KEY"] = "3da6df61b42b2e2d0e6feb98912abb4f31028e04"
os.environ["OPENAI_API_KEY"] = "sk-proj-OEjgSk0FDWF0kFKNlECwT3BlbkFJemihvOFiziPy7dLt9omO"

dataset_disc = """
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


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        "customer_name": "irtika",
        "customer_info": "The customer transaction history can be accessed using file_read_tool, this is the dataset description: \n" + dataset_disc,
        "topic": "Anti-money laundering",
    }
    FraudDetectorCrew().crew().kickoff(inputs=inputs)
    
def run_crew(customer_name, customer_info, topic, dataset_path):
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        "customer_name": customer_name,
        "customer_info": customer_info,
        "topic": topic,
    }

    # Update the file path in crew.py to point to the uploaded file
    FraudDetectorCrew.file_path = dataset_path

    # Run the crew
    crew_instance = FraudDetectorCrew().crew()
    results = crew_instance.kickoff(inputs=inputs)
    return results


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "customer_name": "John Doe",
        "customer_info": "The customer transaction history can be accessed using file_read_tool",
        "topic": "Credit card",
    }
    try:
        FraudDetectorCrew().crew().train(
            n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        FraudDetectorCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "customer_name": "John Doe",
        "customer_info": "Company Enterprise",
        "topic": "AI Agents",
    }
    try:
        FraudDetectorCrew().crew().test(
            n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs
        )

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


if __name__ == "__main__":
    run()
