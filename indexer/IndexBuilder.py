from Storage import Storage
from stopwords import stop_words_slovene
import numpy as np

DB_NAME = 'inverted-index.db'


class IndexBuilder:
    def __init__(self, documents):
        # create new db instance
        self.storage = Storage(DB_NAME)

        # create the tables if they do not exist
        self.storage.create_tables()

        self.documents = documents

        # create index from processed documents
        self.build_index()

    def build_index(self):
        for document in self.documents:

            # transform all words in document to lowercase before indexing
            lowercase_content = [x.lower() for x in document['content']]

            for word in lowercase_content:
                if word not in stop_words_slovene:
                    # finds all occurences of the word in the document
                    occurrence_index = np.where(np.array(lowercase_content) == word)[0]

                    frequency = len(occurrence_index)

                    self.storage.insert_index_word(word, document['name'], frequency,
                                                   self.indexes_to_string(occurrence_index))

        self.storage.close_connection()

    # transform array of indexes to comma separated string
    def indexes_to_string(self, indexes):
        index_string = ''

        for index in np.nditer(indexes):
            index_string += '{},'.format(str(index))

        # remove last comma character
        index_string = index_string[:-1]

        return index_string
