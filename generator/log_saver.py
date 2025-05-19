import json
import os

def save_log(log, filename="output/generated_log.jsonocel"):
    """
    Saves the OCEL log to a .jsonocel file with pretty formatting.

    Args:
        log (dict): The full OCEL log
        filename (str): Destination path and filename
    """
    dir_path = os.path.dirname(filename)
    if dir_path:  # Only create if there's a directory specified
        os.makedirs(dir_path, exist_ok=True)

    with open(filename, "w") as f:
        json.dump(log, f, indent=2)
    print(f"\n✅ Log saved to '{filename}'")
