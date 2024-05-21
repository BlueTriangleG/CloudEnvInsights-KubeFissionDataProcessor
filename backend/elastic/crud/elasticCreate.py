def create_handler(context):
    import json
    from elasticsearch import Elasticsearch
    from utils.validation import validate_data

    req = json.loads(context.request.body)
    es_url = req.get('url')
    data = req.get('data')

    es = Elasticsearch([es_url])

    index_name = data.get('index', 'not_found_index')
    if index_name == 'not_found_index':
        return json.dumps({"error": "Index not found in data."})
    else:
        data.pop('index', None)

    # validation
    valid, error_message = validate_data(es, index_name, data)
    if not valid:
        return json.dumps({"error": error_message})

    # insert
    try:
        response = es.index(index=index_name, body=data)
        return json.dumps({"result": "created", "response": response})
    except Exception as e:
        return json.dumps({"error": str(e)})


