def delete_handler(context):
    import json
    from elasticsearch import Elasticsearch
    
    req = json.loads(context.request.body)
    es_url = req.get('url')
    data = req.get('data')

    es = Elasticsearch([es_url])

    index_name = data.get('index', 'not_found_index')
    doc_id = data.get('id', 'not_found_id')

    if index_name == 'not_found_index' or doc_id == 'not_found_id':
        return json.dumps({"error": "Index or ID not found in data."})
    
    # delete
    try:
        response = es.delete(index=index_name, id=doc_id)
        return json.dumps({"result": "deleted", "response": response})
    except Exception as e:
        return json.dumps({"error": str(e)})
