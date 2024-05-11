def update_handler(context, url: str):
    import json
    from elasticsearch import Elasticsearch
    from datetime import datetime

    es = Elasticsearch([url])

    # read json
    data = json.loads(context.request.body)
    doc_id = data.pop('id', None)
    date_arg = data.get('date', datetime.now().strftime('%Y-%m'))
    year, month = date_arg.split('-')
    index_name = f"weather_conditions_{year}_{month}"

    # update
    try:
        response = es.update(index=index_name, id=doc_id, body={"doc": data})
        return json.dumps({"result": "updated", "response": response})
    except Exception as e:
        return json.dumps({"error": str(e)})

