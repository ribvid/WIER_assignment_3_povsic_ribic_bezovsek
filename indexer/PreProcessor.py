from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from stopwords import stop_words_slovene


class PreProcessor:
    def __init__(self):
        pass

    @staticmethod
    def tokenize_documents(documents):
        processed_documents = []

        for document in documents:
            document['content'] = PreProcessor.tokenize_document(document['content'])

            processed_documents.append(document)

        return processed_documents

    @staticmethod
    def remove_markups(content):
        soup = BeautifulSoup(content, "html.parser")

        for s in soup(['script', 'style']):
            s.decompose()

        return ' '.join(soup.stripped_strings)

    @staticmethod
    def tokenize_document(content):
        clean_doc = PreProcessor.remove_markups(content)

        return word_tokenize(clean_doc)

    @staticmethod
    def remove_stopwords(tokenized_content, convert_to_lower=False):
        filtered_content = []

        for word in tokenized_content:
            if word not in stop_words_slovene:
                filtered_content.append(word if not convert_to_lower else word.lower())

        return filtered_content