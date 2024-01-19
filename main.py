import os
import xmltodict
import json
from cron_translate import extractDetails
import pandas as pd

folderPath = '/Users/balamurugan/Desktop/RunDeck/Input_XML'
outputFilePath = '/Users/balamurugan/Desktop/RunDeck/output_jobs.xlsx'
inputJsonPath = '/Users/balamurugan/Desktop/RunDeck/Json_File/input_json.json'
finalJson = {}

# Converting Input Xml into Json Format
def convertXmlToJson(xml_file_path):
    with open(xml_file_path, 'r') as xml_file:
        xml_data = xml_file.read()
    xml_dict = xmltodict.parse(xml_data)
    return json.dumps(xml_dict)

# Accessing the Input Folder and reading each Xml file
def processFolder(folder_path):
    json_data = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".xml"):
            xml_file_path = os.path.join(folder_path, filename)
            json_data.append({
                'filename': filename,
                'json_data': convertXmlToJson(xml_file_path)
            })
    return json_data

result = processFolder(folderPath)

for item in result:
    try:
        json_data_dict = json.loads(item['json_data'])
        # json_data_dict = json_data_dict['joblist']['job']['schedule']
        finalJson[item['filename'][:-4]] = json_data_dict
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing {item['filename']}: {e}")

jsonObject = json.dumps(finalJson,indent=4)
with open(inputJsonPath, "w") as outfile:
    outfile.write(jsonObject)
finalJson = extractDetails(finalJson)

df = pd.DataFrame.from_dict(finalJson, orient='index')
df.to_excel(outputFilePath, index=False)

print("Operation Completed .... Output is written in file --> " + outputFilePath )