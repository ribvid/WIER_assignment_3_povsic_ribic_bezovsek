import os
from datetime import datetime
from PreProcessor import PreProcessor
from tabulate import tabulate


class ClassicSearch:
    def __init__(self, documents_folder):
        self.documents_folder = documents_folder
        self.preprocessor = PreProcessor()

    def search(self, query, max_results_to_show):
        start_time = datetime.now()

        query = query.split(" ")

        documents = []

        directory = sorted([fol for fol in os.listdir(self.documents_folder) if os.path.isdir(os.path.join(self.documents_folder, fol))])

        for folder in directory:
            documents_sub_folder = r'%s/%s' % (self.documents_folder, folder)
            sub_folder_content = [file for file in os.listdir(documents_sub_folder) if file.endswith('.html')]

            for document_name in sub_folder_content:

                html_file = r'%s/%s' % (documents_sub_folder, document_name)

                try:
                    document = open(html_file, mode='r', encoding="utf8").read()
                    tokenized_document = self.preprocessor.tokenize_document(document)
                    preprocessed_document = self.preprocessor.remove_stopwords(tokenized_document, convert_to_lower=True)

                    if any(word in preprocessed_document for word in query):
                        documents.append({
                            "frequency": sum(preprocessed_document.count(word) for word in query),
                            "content": tokenized_document,
                            "name": document_name,
                        })

                except Exception as error:
                    print('An exception occured while parsing page ', document_name)
                    print(error)

        results = []

        for document in sorted(documents, key=lambda k: k["frequency"], reverse=True)[:max_results_to_show]:
            results.append([document["frequency"], document["name"], self.create_snippet(query, document["content"])])

        end_time = datetime.now()

        time_difference = end_time - start_time

        print("[CLASSIC SEARCH] Results for a query " + " ".join(query))

        if len(documents) <= 0:
            print("     The search took {}s".format(time_difference.total_seconds()))
            print("     No results found :(\n")
        else:
            print("     Results found in {}s".format(time_difference.total_seconds()))
            print(tabulate(results, headers=["Frequencies", "Document", "Snippet"]))

        print("\n\n")

    def create_snippet(self, query, document):
        snippet = ""

        for index, element in enumerate(document):
            if any(word == element.lower() for word in query):
                snippet = snippet + " ... " + " ".join(document[max(index - 3, 0):min(index + 4, len(document))])

        return snippet + " ..."
