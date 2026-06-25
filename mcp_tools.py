from langchain.tools import tool
import json

@tool
def get_live_machine_status(machine_id: str) -> str:
    """
    Fetches the live status, temperature, and error codes of a given engineering machine.
    Use this tool when the user asks for the CURRENT status or live parameters of a machine.
    """
    # This is our mock live database. In a real company, this connects to a SQL DB or IoT API.
    mock_db = {
        "Machine A": {
            "status": "Error", 
            "temperature": "85C", 
            "spark_gap": "Fluctuating", 
            "error_code": "ERR-702"
        },
        "Machine B": {
            "status": "Running", 
            "temperature": "45C", 
            "spark_gap": "0.05mm", 
            "error_code": "None"
        }
    }
    
    # Clean the input (e.g., convert "machine a" to "Machine A")
    machine_id = machine_id.title()
    
    if machine_id in mock_db:
        return json.dumps(mock_db[machine_id])
    else:
        return f"Machine '{machine_id}' not found in the live monitoring system."