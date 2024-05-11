def read_handler(context, url: str):
    import json
    from elasticsearch import Elasticsearch
    from datetime import datetime

    es = Elasticsearch([url])

    # read from URL
    doc_id = context.request.args.get('id')
    date_arg = context.request.args.get('date')  # 期望格式为 'YYYY-MM'

    # extract index
    if date_arg:
        year, month = date_arg.split('-')
    else:
        now = datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
    index_name = f"weather_conditions_{year}_{month}"

    # read
    try:
        response = es.get(index=index_name, id=doc_id)
        return json.dumps({"result": "retrieved", "response": response['_source']})
    except Exception as e:
        return json.dumps({"error": str(e)})


