"""
DBpedia SPARQL querying + offline filtering.
In demo mode, uses offline candidates and filters them.
In online mode, builds a SPARQL query (requires internet).
"""

import requests
import urllib.parse


class SparqlClient:
    def __init__(self, mode="demo", endpoint="https://dbpedia.org/sparql", limit=50):
        self.mode = mode
        self.endpoint = endpoint
        self.limit = limit

    def filter_candidates(self, candidates, answers):
        if self.mode == "demo":
            return self._filter_offline(candidates, answers)
        return self._filter_online(candidates, answers)

    def _filter_offline(self, candidates, answers):
        filtered = []
        for c in candidates:
            keep = True
            for k, v in answers.items():
                if v == "unknown":
                    continue
                if c.get(k, None) is None:
                    continue
                if isinstance(v, bool):
                    # normalize truthy vs value
                    val = c.get(k)
                    if isinstance(val, bool):
                        if val != v:
                            keep = False
                            break
                    else:
                        if bool(val) != v:
                            keep = False
                            break
                else:
                    if str(c.get(k)).lower() != str(v).lower():
                        keep = False
                        break
            if keep:
                filtered.append(c)
        return filtered

    def _filter_online(self, candidates, answers):
        # Simplified: we query DBpedia for candidates matching filters,
        # then intersect with current candidate set by name (label).
        if not answers:
            return candidates
        filters = []
        for k, v in answers.items():
            if v == "unknown":
                continue
            if isinstance(v, bool):
                v = "true" if v else "false"
            filters.append((k, v))
        if not filters:
            return candidates

        query = self._build_query(filters)
        try:
            res = requests.get(self.endpoint, params={"query": query, "format": "application/sparql-results+json"}, timeout=10)
            res.raise_for_status()
            data = res.json()
            names = set()
            for b in data.get("results", {}).get("bindings", []):
                label = b.get("label", {}).get("value")
                if label:
                    names.add(label.lower())
            # Intersect by name (lowercase)
            filtered = [c for c in candidates if c.get("name", "").lower() in names]
            return filtered if filtered else candidates
        except Exception:
            # On failure, return existing candidates to keep the game going.
            return candidates

    def _build_query(self, filters):
        # Very basic pattern: match ?person with optional filters as literal matches
        where = []
        for k, v in filters:
            where.append(f'?person <http://example.org/{k}> "{v}" .')
        where_clause = "\n".join(where)
        q = f"""
        SELECT DISTINCT ?person ?label WHERE {{
            {where_clause}
            ?person rdfs:label ?label .
            FILTER (lang(?label) = 'en')
        }}
        LIMIT {self.limit}
        """
        return q