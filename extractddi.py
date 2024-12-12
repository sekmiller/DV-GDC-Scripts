import requests
import xml.etree.ElementTree as ET
import json


# Define a function to fetch XML from an API, parse it, and write to JSON
def parse_xml_from_api_to_json(api_url, json_file):
    try:
        # Fetch the XML data from the API
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Parse the XML content
        root = ET.fromstring(response.content)

        # Define the namespace for DDI Codebook
        ns = {'ddi': 'ddi:codebook:2_5'}
        file_name = None
        doi = None
        keyword = None

        # Extract file name
        file_dscr = root.find(".//ddi:fileDscr", ns)
        if file_dscr is not None:
            file_name_elem = file_dscr.find(".//ddi:fileTxt/ddi:fileName", ns)
            if file_name_elem is not None:
                file_name = file_name_elem.text

        # Extract DOI
        doi_elem = root.find(".//ddi:docDscr/ddi:citation/ddi:titlStmt/ddi:IDNo", ns)
        if doi_elem is not None:
            doi = doi_elem.text

        # Extract keyword
        keyword_elem = root.find(".//ddi:stdyDscr/ddi:stdyInfo/ddi:subject/ddi:keyword", ns)
        if keyword_elem is not None:
            keyword = keyword_elem.text

        # Initialize a list to store the extracted data
        variables = {}
        # Find all 'var' elements under 'dataDesc'

        # Extract variables
        for data_desc in root.findall(".//ddi:dataDscr", ns):
            for var in data_desc.findall(".//ddi:var", ns):
                # Extract the 'name' and 'type' attributes
                name = var.get('name')
                var_type = var.get('labl')

                # Use a default key if 'name' is None
                if name is None:
                    name = f"unknown_variable_{len(variables) + 1}"  # Unique default name

                # Add the variable data to the dictionary
                print(name)
                variables[name] = {
                    "name": var_type if var_type else "unknown_type",
                    "description": var_type if var_type else "unknown_description",
                    "nlSentences": ["Natural Language cues."],
                    "group": keyword if keyword else "HDV"
                }
                print(variables)

        output_data = {
            "inputFiles": {
                file_name if file_name else "unknown_file": {  # Use "unknown_file" if file_name is None
                    "entityType": "country",
                    "provenance": doi if doi else "unknown_DOI"  # Use "unknown_DOI" if DOI is None
                }
            },
            "variables": variables,
            "sources": {
                doi if doi else "unknown_DOI": {  # Use "unknown_DOI" if DOI is None
                    "url": "https://dataverse.harvard.edu",
                    "provenances": {
                        doi if doi else "unknown_DOI": "https://dataverse.harvard.edu"
                    }
                }
            }
        }

        # Write the data to a JSON file
        output_file = 'formatted_output.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4, ensure_ascii=False)

        print(f"Data successfully written to {json_file}")

    except requests.exceptions.RequestException as req_err:
        print(f"HTTP Request error: {req_err}")

    except ET.ParseError as parse_err:
        print(f"XML Parse error: {parse_err}")
    except Exception as e:
         print(f"An unexpected error occurred: {e}")

# API URL and output JSON file
api_url = 'https://dataverse.harvard.edu/api/datasets/export?exporter=ddi&persistentId=doi:10.7910/DVN/1U75SU'
json_file = 'output.json'  # Replace with your desired JSON file path

# Call the function
parse_xml_from_api_to_json(api_url, json_file)
