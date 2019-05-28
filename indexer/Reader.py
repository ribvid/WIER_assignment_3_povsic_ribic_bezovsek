import os


class Reader:
    def __init__(self, folder):
        self.documents_folder = folder

    def get_documents(self):
        documents = []
        total_documents_counter = 0

        directory = [fol for fol in os.listdir(self.documents_folder) if
                     os.path.isdir(os.path.join(self.documents_folder, fol))]
        directory = sorted(directory)

        for folder in directory:
            documents_counter = 0

            documents_sub_folder = r'%s/%s' % (self.documents_folder, folder)
            sub_folder_content = [file for file in os.listdir(documents_sub_folder) if file.endswith('.html')]

            for document in sub_folder_content:

                html_file = r'%s/%s' % (documents_sub_folder, document)

                try:
                    documents.append({"name": document, "content": open(html_file, mode='r', encoding="utf8").read()})
                    total_documents_counter += 1
                    documents_counter += 1

                except Exception as error:
                    print('An exception occured while parsing page ', document)
                    print(error)

            print('________________________________________________________________________________________\n')
            print(' FETCHED ' + str(documents_counter) + ' PAGES INSIDE ' + folder + ' FOLDER \n')

        print('________________________________________________________________________________________\n')
        print('FETCHED ' + str(total_documents_counter) + ' TOTAL NEW PAGES\n')

        return documents
