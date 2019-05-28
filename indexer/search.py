from DataRetrieval import DataRetrieval
from ClassicSearch import ClassicSearch

search_queries = [
    "predelovalne dejavnosti",
    "trgovina",
    "social services",
    "Sistem SPOT",
    "EU Parlament",
    "VLADA REPUBLIKE SLOVENIJE"
]

data_retrieval = DataRetrieval()
classic_search = ClassicSearch('pages')

for search_query in search_queries:
    data_retrieval.search(query=search_query, max_results_to_show=5)
    classic_search.search(query=search_query, max_results_to_show=5)
