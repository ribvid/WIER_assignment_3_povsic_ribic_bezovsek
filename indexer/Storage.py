import sqlite3


class Storage:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)

    def create_tables(self):
        c = self.conn.cursor()

        c.execute('''
            CREATE TABLE IF NOT EXISTS IndexWord (
                word TEXT PRIMARY KEY
            );
        ''')

        c.execute('''
            CREATE TABLE IF NOT EXISTS Posting (
                word TEXT NOT NULL,
                documentName TEXT NOT NULL,
                frequency INTEGER NOT NULL,
                indexes TEXT NOT NULL,
                PRIMARY KEY (word, documentName),
                FOREIGN KEY (word) REFERENCES IndexWord(word)
            );
        ''')

        self.conn.commit()

        self.remove_data()

        # self.conn.close()

    def remove_data(self):
        c = self.conn.cursor()

        c.execute('''DELETE FROM IndexWord''')
        c.execute('''DELETE FROM Posting''')

    def insert_index_word(self, word, document_name, frequency, occurence_indexes):
        c = self.conn.cursor()

        c.execute('''
            INSERT INTO IndexWord (word)
            SELECT ?
            WHERE NOT EXISTS(SELECT 1 FROM IndexWord WHERE word = ?);
        ''', (word, word))

        self.insert_posting(word, document_name, frequency, occurence_indexes)

        self.conn.commit()
        # self.conn.close()

    def insert_posting(self, word, document_name, frequency, indexes):
        c = self.conn.cursor()

        c.execute('''
            INSERT INTO Posting (word, documentName, frequency, indexes)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS(SELECT 1 FROM Posting WHERE word = ? AND documentName = ?);
        ''', (word, document_name, frequency, indexes, word, document_name))

        self.conn.commit()
        # self.conn.close()

    def update_posting(self, word, document_name):
        c = self.conn.cursor()

        c.execute('''
            INSERT OR IGNORE INTO Posting (word, documentName, frequency, indexes) VALUES (?, ?, ?, ?)
            UPDATE Posting SET frequency = ? WHERE word = ? AND documentName = ? 
        ''', ())

    def find_word_postings(self, word):
        c = self.conn.cursor()

        cursor = c.execute('''
                    SELECT * FROM Posting
                    WHERE word = ?
                ''', (word,))

        return cursor.fetchall()

    def close_connection(self):
        self.conn.close()

