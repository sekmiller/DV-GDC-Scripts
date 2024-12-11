import pandas as pd
import json
import argparse


def reorder_csv(input_csv, output_csv, column_order):
    """
    Reorders columns in a CSV based on the specified column order.

    Args:
    - input_csv (str): Path to the input CSV file.
    - output_csv (str): Path to the output CSV file.
    - column_order (list of int): Order of column indices (e.g., [2, 0, 1]).
    """
    df = pd.read_csv(input_csv)
    reordered_df = df[[df.columns[i] for i in column_order]]
    reordered_df.to_csv(output_csv, index=False)
    print(f"CSV columns reordered and saved to {output_csv}")


def update_json(target_json, update_json, output_json):
    """
    Updates the target JSON file with data from the update JSON file.

    Args:
    - target_json (str): Path to the target JSON file to update.
    - update_json (str): Path to the JSON file containing updates.
    - output_json (str): Path to save the updated JSON file.
    """
    with open(target_json, 'r') as f:
        target_data = json.load(f)

    with open(update_json, 'r') as f:
        update_data = json.load(f)

    # Update target JSON with values from update JSON
    def recursive_update(target, updates):
        for key, value in updates.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                recursive_update(target[key], value)
            else:
                target[key] = value

    recursive_update(target_data, update_data)

    with open(output_json, 'w') as f:
        json.dump(target_data, f, indent=4)

    print(f"JSON updated and saved to {output_json}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Process CSV and update JSON files.")

    # CSV reordering arguments
    parser.add_argument("--input_csv", required=True, help="Path to the input CSV file")
    parser.add_argument("--output_csv", required=True, help="Path to the output CSV file")
    parser.add_argument("--column_order", required=True, help="Comma-separated column order, e.g., '2,0,1'")

    # JSON updating arguments
    parser.add_argument("--target_json", required=True, help="Path to the target JSON file")
    parser.add_argument("--update_json", required=True, help="Path to the JSON file with updates")
    parser.add_argument("--output_json", required=True, help="Path to save the updated JSON file")

    # Parse the arguments
    args = parser.parse_args()

    # Convert column_order from a comma-separated string to a list of integers
    column_order = list(map(int, args.column_order.split(",")))

    # Run the CSV reordering
    reorder_csv(args.input_csv, args.output_csv, column_order)

    # Run the JSON update
    update_json(args.target_json, args.update_json, args.output_json)
