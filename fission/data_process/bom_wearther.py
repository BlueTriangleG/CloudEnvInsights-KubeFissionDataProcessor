import json, requests

bom_data_mel = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()
bom_data_geelong = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94857.json').json()

file_path_mel = "bom_mel.json"
file_path_gee = 'bom_gee.json'

# 存数据
with open(file_path_mel, "w") as json_file:
    json.dump(bom_data_mel , json_file)

with open(file_path_gee, "w") as json_file:
    json.dump(bom_data_geelong , json_file)