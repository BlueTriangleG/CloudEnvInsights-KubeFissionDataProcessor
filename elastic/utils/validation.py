def generate_template(properties):
    template = {}
    for field, specs in properties.items():
        field_type = specs['type']
        if field_type == 'text' or field_type == 'keyword':
            template[field] = "string"
        elif field_type == 'integer':
            template[field] = 0
        elif field_type == 'float':
            template[field] = 0.0
        elif field_type == 'date':
            template[field] = "yyyy-MM-dd-HH"
    return template

def validate_data(es, index_name, data):
    import json

    try:
        mappings = es.indices.get_mapping(index=index_name)
        properties = mappings[index_name]['mappings']['properties']
        
        for field, value in data.items():
            if field not in properties:
                template = generate_template(properties)
                return False, f"Field {field} not defined in index mappings. Correct format: {json.dumps(template, indent=2)}"
            field_type = properties[field]['type']
            
            if field_type == 'text' and not isinstance(value, str):
                template = generate_template(properties)
                return False, f"Field {field} should be of type text. Correct format: {json.dumps(template, indent=2)}"
            elif field_type == 'keyword' and not isinstance(value, str):
                template = generate_template(properties)
                return False, f"Field {field} should be of type keyword. Correct format: {json.dumps(template, indent=2)}"
            elif field_type == 'integer' and not isinstance(value, int):
                template = generate_template(properties)
                return False, f"Field {field} should be of type integer. Correct format: {json.dumps(template, indent=2)}"
            elif field_type == 'float' and not isinstance(value, (float, int)):  # allow int as float
                template = generate_template(properties)
                return False, f"Field {field} should be of type float. Correct format: {json.dumps(template, indent=2)}"
            elif field_type == 'date' and not isinstance(value, str):  # Simple check for date format
                template = generate_template(properties)
                return False, f"Field {field} should be of type date. Correct format: {json.dumps(template, indent=2)}"
        
        return True, ""
    except Exception as e:
        return False, str(e)