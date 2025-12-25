"""
DBpedia SPARQL querying + offline filtering.
Simplified and robust approach for 20 Questions AI.
"""

import requests

class SparqlClient:
    COUNTRY_TO_CONTINENT = {
        "United States": "Americas", "Canada": "Americas", "Mexico": "Americas", "Brazil": "Americas",
        "Argentina": "Americas", "Colombia": "Americas", "Chile": "Americas", "Peru": "Americas",
        "Jamaica": "Americas", "Cuba": "Americas", "Trinidad and Tobago": "Americas",
        "France": "Europe", "Germany": "Europe", "United Kingdom": "Europe", "Italy": "Europe", "Spain": "Europe",
        "Poland": "Europe", "Sweden": "Europe", "Norway": "Europe", "Finland": "Europe", "Denmark": "Europe",
        "Greece": "Europe", "Portugal": "Europe", "Netherlands": "Europe", "Belgium": "Europe", "Switzerland": "Europe",
        "Austria": "Europe", "Hungary": "Europe", "Czech Republic": "Europe", "Ukraine": "Europe",
        "Russia": "Europe", "Romania": "Europe", "Ireland": "Europe", "Croatia": "Europe", "Serbia": "Europe",
        "China": "Asia", "India": "Asia", "Japan": "Asia", "South Korea": "Asia", "Vietnam": "Asia",
        "Pakistan": "Asia", "Indonesia": "Asia", "Philippines": "Asia", "Turkey": "Asia",
        "Iran": "Asia", "Iraq": "Asia", "Saudi Arabia": "Asia", "Israel": "Asia",
        "South Africa": "Africa", "Nigeria": "Africa", "Egypt": "Africa", "Kenya": "Africa", "Ethiopia": "Africa",
        "Morocco": "Africa", "Ghana": "Africa", "Algeria": "Africa",
        "Australia": "Oceania", "New Zealand": "Oceania"
    }

    def __init__(self, mode="demo", endpoint="https://dbpedia.org/sparql", limit=100):
        self.mode = mode
        self.endpoint = endpoint
        self.limit = limit

    def filter_candidates(self, candidates, answers, properties=None):
        """Filter candidates based on user answers."""
        return self._filter_offline(candidates, answers)

    def expand_search(self, answers, properties):
        """Fetch new candidates from DBpedia based on known answers."""
        # Build simple SPARQL query based on core answers
        is_alive = answers.get("alive")
        is_fictional = answers.get("fictional", False)
        gender = answers.get("gender")
        
        # Determine base class
        base_class = "dbo:FictionalCharacter" if is_fictional is True else "dbo:Person"
        
        # Build filter clauses
        filters = []
        if is_alive is True:
            filters.append("NOT EXISTS { ?person dbo:deathDate ?d }")
        elif is_alive is False:
            filters.append("EXISTS { ?person dbo:deathDate ?d }")
        
        if gender and gender != "unknown":
            if isinstance(gender, str):
                filters.append(f"EXISTS {{ ?person foaf:gender ?g . FILTER(contains(lcase(str(?g)), '{gender.lower()}')) }}")
        
        filter_str = " && ".join(filters) if filters else ""
        filter_clause = f"FILTER({filter_str})" if filter_str else ""
        
        query = f"""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT DISTINCT ?person ?label ?death WHERE {{
            ?person a {base_class} .
            ?person rdfs:label ?label .
            FILTER (lang(?label) = 'en')
            OPTIONAL {{ ?person dbo:deathDate ?death }}
            {filter_clause}
        }} LIMIT 200
        """
        
        print(f"DEBUG EXPANSION: Query filters = {filters}")
        print(f"DEBUG EXPANSION: Base class = {base_class}")
        
        try:
            res = requests.get(self.endpoint, params={"query": query, "format": "application/sparql-results+json"}, timeout=30)
            if res.status_code != 200:
                return []
            
            data = res.json()
            candidates = []
            for b in data.get("results", {}).get("bindings", []):
                name = b.get("label", {}).get("value")
                uri = b.get("person", {}).get("value")
                death = b.get("death", {}).get("value")
                if name and uri:
                    c = {
                        "name": name,
                        "uri": uri,
                        "alive": False if death else True,
                        "fictional": is_fictional if isinstance(is_fictional, bool) else False,
                        "popularity": 0
                    }
                    candidates.append(c)
            
            # Fill in properties for these candidates
            if candidates:
                print(f"DEBUG EXPANSION: Fetched {len(candidates)} raw candidates")
                candidates = self._fill_properties(candidates, properties or [])
                # Filter based on all answers
                pre_filter_count = len(candidates)
                candidates = self._filter_offline(candidates, answers, strict=False)
                print(f"DEBUG EXPANSION: After filter {pre_filter_count} -> {len(candidates)}")
            
            return candidates[:50]
        except Exception as e:
            return []

    def _fill_properties(self, candidates, properties):
        """Batch fetch properties for candidates from DBpedia."""
        if not candidates:
            return []
        
        uri_to_cand = {c["uri"]: c for c in candidates}
        batch_size = 20
        uri_list = list(uri_to_cand.keys())
        
        for i in range(0, len(uri_list), batch_size):
            batch = uri_list[i:i+batch_size]
            uris = " ".join([f"<{u}>" for u in batch])
            
            query = f"""
            PREFIX dbo: <http://dbpedia.org/ontology/>
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?person ?prop ?val ?bp_country ?nat_label WHERE {{
                VALUES ?person {{ {uris} }}
                ?person ?p_uri ?o .
                OPTIONAL {{ ?o rdfs:label ?label . FILTER(lang(?label) = 'en') }}
                BIND(IF(isLiteral(?o), str(?o), IF(bound(?label), str(?label), str(?o))) AS ?val)
                VALUES (?p_uri ?prop) {{
                    (foaf:gender "gender") (dbo:occupation "occupation")
                    (dbo:nationality "nationality") (dbo:field "field")
                    (dbo:birthPlace "born_in") (dbo:knownFor "known_for")
                }}
                OPTIONAL {{
                    ?person dbo:birthPlace ?bp .
                    ?bp dbo:country ?country_res .
                    ?country_res rdfs:label ?bp_country .
                    FILTER(lang(?bp_country) = 'en')
                }}
                OPTIONAL {{
                    ?person dbo:nationality ?nat .
                    ?nat rdfs:label ?nat_label .
                    FILTER(lang(?nat_label) = 'en')
                }}
            }}
            """
            try:
                res = requests.get(self.endpoint, params={"query": query, "format": "application/sparql-results+json"}, timeout=25)
                if res.status_code == 200:
                    data = res.json()
                    for b in data.get("results", {}).get("bindings", []):
                        u = b["person"]["value"]
                        if u not in uri_to_cand:
                            continue
                        
                        if "prop" in b and "val" in b:
                            p, v_raw = b["prop"]["value"], b["val"]["value"]
                            v = self._clean_value(v_raw)
                            if v != "unknown" and p not in uri_to_cand[u]:
                                uri_to_cand[u][p] = v
                        
                        if "bp_country" in b:
                            uri_to_cand[u]["country"] = b["bp_country"]["value"]
                        
                        if "nat_label" in b:
                            uri_to_cand[u]["nationality"] = b["nat_label"]["value"]
                        
                        # Infer continent
                        inf_country = uri_to_cand[u].get("country", "")
                        inf_nat = uri_to_cand[u].get("nationality", "")
                        for c_key, cont in self.COUNTRY_TO_CONTINENT.items():
                            if c_key.lower() in inf_country.lower() or c_key.lower() in inf_nat.lower():
                                uri_to_cand[u]["continent"] = cont
                                break
            except:
                continue
        
        return candidates

    def _clean_value(self, v):
        """Clean DBpedia value artifacts."""
        if not v:
            return "unknown"
        res = v.split("/")[-1].replace("_", " ").strip()
        blacklist = ["personfunction", "list of ", "template:", "category:"]
        for b in blacklist:
            if b in res.lower():
                return "unknown"
        if any(c.isdigit() for c in res) and len(res) > 20 and "-" in res:
            return "unknown"
        return res

    def _filter_offline(self, candidates, answers, strict=False):
        """Filter candidates locally based on answers."""
        filtered = []
        
        for c in candidates:
            keep = True
            for k, v in answers.items():
                if v == "unknown":
                    continue
                
                cand_val = c.get(k, "unknown")
                if cand_val is None:
                    cand_val = "unknown"
                
                # Normalize for comparison
                if isinstance(cand_val, bool):
                    cand_str = "true" if cand_val else "false"
                else:
                    cand_str = str(cand_val).lower()
                
                # Skip unknown values unless strict mode
                if cand_str == "unknown":
                    if strict:
                        keep = False
                        break
                    continue
                
                # Check match
                if not self._match(cand_str, v, k):
                    keep = False
                    break
            
            if keep:
                filtered.append(c)
        
        return filtered

    def _match(self, cand_val, constraint, key=None):
        """Check if candidate value matches constraint."""
        constraints = constraint if isinstance(constraint, list) else [constraint]
        
        def normalize_gender(g):
            g = str(g).lower()
            if g in ["male", "man", "masculine"]:
                return "male"
            if g in ["female", "woman", "feminine"]:
                return "female"
            return g
        
        for cond in constraints:
            is_not = False
            target = cond
            if isinstance(cond, tuple) and cond[0] == 'NOT':
                is_not = True
                target = cond[1]
            
            # Determine match
            match = False
            if isinstance(target, bool):
                b_val = cand_val == "true"
                match = (b_val == target)
            elif key == "gender":
                match = (normalize_gender(cand_val) == normalize_gender(target))
            else:
                match = (str(target).lower() in cand_val)
            
            if is_not and match:
                return False
            if not is_not and not match:
                return False
        
        return True
