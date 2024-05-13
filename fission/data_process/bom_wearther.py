import json, requests

bom_data_mel = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json').json()['observations']['data']
bom_data_geelong = requests.get('http://reg.bom.gov.au/fwo/IDV60901/IDV60901.94857.json').json()['observations']['data']

file_path_mel = "bom_mel_realTime.json"
# file_path_gee = 'bom_gee_realTime.json'

# 存数据
with open(file_path_mel, "w") as json_file:
    json.dump(bom_data_mel , json_file)

# with open(file_path_gee, "w") as json_file:
#     json.dump(bom_data_geelong , json_file)