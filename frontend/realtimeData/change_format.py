import json

# 读取文件并逐行解析 JSON 对象
with open("output.json", "r") as file:
    data = [json.loads(line) for line in file]

# 格式化数据
formatted_data = [
    {
        "_index": "mastodon-aus-social",
        "_id": item["id"],
        "_score": 1.0,
        "_source": {
            "id": item["id"],
            "created_at": item["created_at"],
            "lang": item["lang"],
            "sentiment": item["sentiment"],
            "tokens": item["tokens"],
            "tags": item["tags"]
        }
    } for item in data
]

# 将结果写入新的 JSON 文件
json_output = json.dumps(formatted_data, indent=4)
with open("output_formatted.json", "w") as f:
    f.write(json_output)