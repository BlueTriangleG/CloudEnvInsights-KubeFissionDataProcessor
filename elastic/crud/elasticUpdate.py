def update_handler(context):
    import json
    from elasticsearch import Elasticsearch
    from utils.validation import validate_data

    req = json.loads(context.request.body)
    es_url = req.get('url')
    data = req.get('data')

    es = Elasticsearch([es_url])

    index_name = data.get('index', 'not_found_index')
    doc_id = data.get('id', 'not_found_id')
    doc_data = data.get('doc', 'not_found_doc')

    if index_name == 'not_found_index' or doc_id == 'not_found_id' or doc_data == 'not_found_doc':
        return json.dumps({"error": "Index, ID, or document data not found in data."})
    
    # validation
    valid, error_message = validate_data(es, index_name, doc_data)
    if not valid:
        return json.dumps({"error": error_message})

    # update
    try:
        response = es.update(index=index_name, id=doc_id, body={"doc": doc_data})
        return json.dumps({"result": "updated", "response": response})
    except Exception as e:
        return json.dumps({"error": str(e)})

