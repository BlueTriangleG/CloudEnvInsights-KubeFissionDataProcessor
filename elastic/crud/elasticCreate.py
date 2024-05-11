def create_handler(context, url: str):
    import json
    from elasticsearch import Elasticsearch
    from datetime import datetime

    es = Elasticsearch([url])

    # read json
    data = json.loads(context.request.body)
    date_arg = data.get('date', datetime.now().strftime('%Y-%m'))
    year, month = date_arg.split('-')
    index_name = f"weather_conditions_{year}_{month}"

    # create
    try:
        response = es.index(index=index_name, body=data)
        return json.dumps({"result": "created", "response": response})
    except Exception as e:
        return json.dumps({"error": str(e)})

