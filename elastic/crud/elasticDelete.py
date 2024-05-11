def delete_handler(context, url: str):
    import json
    from elasticsearch import Elasticsearch
    from datetime import datetime

    es = Elasticsearch([url])

    # extract index
    doc_id = context.request.args.get('id')
    date_arg = context.request.args.get('date', datetime.now().strftime('%Y-%m'))
    year, month = date_arg.split('-')
    index_name = f"weather_conditions_{year}_{month}"

    # delete
    try:
        response = es.delete(index=index_name, id=doc_id)
        return json.dumps({"result": "deleted", "response": response})
    except Exception as e:
        return json.dumps({"error": str(e)})
