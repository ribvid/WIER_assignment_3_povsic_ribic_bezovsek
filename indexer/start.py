import time

from Reader import Reader
from PreProcessor import PreProcessor
from IndexBuilder import IndexBuilder

# set this to True if you want to drop existing index and create new index in the db
rebuild_index = False

reader = Reader(r'pages')

documents = reader.get_documents()

print("PROCESSING DOCUMENTS...\n")

print("TOKENIZING DOCUMENTS\n")

tokenized_documents = PreProcessor.tokenize_documents(documents)

for doc in tokenized_documents:
    with open('tokenized_pages/' + doc["name"] + '.txt', mode="w", encoding="utf8") as file:
        file.truncate(0)

        file.writelines(token + "\n" for token in doc["content"])

print("DOCUMENTS WERE SUCCESSFULLY TOKENIZED\n")

if rebuild_index:
    print("BUILDING INDEX...")

    start_time = time.time()

    index_builder = IndexBuilder(tokenized_documents)

    end_time = time.time()

    elapsed_time = end_time - start_time

    print("INDEX WAS SUCCESFULLY BUILT IN: " + str(int(elapsed_time / 60)) + " min " + str(int(elapsed_time % 60)) + " sec")

else:
    print("USING ALREADY BUILT INDEX")
