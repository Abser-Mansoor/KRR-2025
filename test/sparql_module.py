# SPARQL filtering module (offline mock for demo)
# Replace with a real SPARQL implementation (sparql_real.py) for DBpedia.

from sample_data import candidates, properties

def execute_sparql(filters):
    """Filter candidates according to filters dict.
    filters example: {'gender': 'male', 'occupation': 'physicist'}
    For demo, require that for each filter key the candidate's property equals the filter value.
    """
    result = []
    for c in candidates:
        match = True
        for prop, val in filters.items():
            # If property missing, fail match
            if prop not in properties.get(c, {}):
                match = False
                break
            if properties[c][prop] != val:
                match = False
                break
        if match:
            result.append(c)
    return result
