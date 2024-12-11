# DV-GDC-Scripts
Scripts for transforming Dataverse Data to be added to Google Data Commons

python scripts for transforming Dataverse data for ingestion into Google Data Commons

This repository is for pilot scripts that transform Dataverse data into files that can be uploaded into the Google Data Commons. The first script (extractddi.py) takes in a ddi export of a datatable and extracts information about the file (name, doi, keywords, variables) and creates a json representation. 

Another script (transformCSV-Config.py) reoders the columns of a datatable to conform to GDC requirements and updates the config.json required for data upload.

See GDC doc here https://docs.datacommons.org/custom_dc/quickstart.html
