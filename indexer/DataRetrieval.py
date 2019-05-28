from datetime import datetime

from Storage import Storage

DB_NAME = "inverted-index.db"


# This class will use the inverted index
class DataRetrieval:
    def __init__(self):
        self.storage = Storage(DB_NAME)

    def search(self, query, max_results_to_show=None):
        start_time = datetime.now()

        query_words = query.lower().split(" ")

        # includes all the postings for all the words in the query
        postings = []

        for word in query_words:
            # finds all the postings for the word and concatenates the two arrays
            postings += self.storage.find_word_postings(word)

        merged_results = self.merge_postings(postings)

        if max_results_to_show is not None:
            merged_results = merged_results[0:max_results_to_show]

        self.get_snippets(merged_results)

        end_time = datetime.now()

        time_difference = end_time - start_time

        self.print_output(query, time_difference, merged_results)

    def merge_postings(self, postings):
        postings_per_site = {}

        # group all the postings by site
        for posting in postings:
            site = posting[1]
            frequency = posting[2]

            if site in postings_per_site:
                postings_per_site[site]["postings"].append(posting)
                postings_per_site[site]["total_frequencies"] += frequency
            else:
                postings_per_site[site] = {
                    "postings": [posting],
                    "site": site,
                    "snippets": None,
                    "total_frequencies": frequency
                }

        list_to_sort = []

        for site in postings_per_site:
            list_to_sort.append(postings_per_site[site])

        # sort the postings that are grouped by site by the total frequencies of words
        sorted_list = sorted(list_to_sort, key=lambda d: d["total_frequencies"], reverse=True)

        return sorted_list

    def get_snippets(self, list_of_results):
        for result in list_of_results:
            positions = []

            snippets = ""

            site = result["site"]

            for posting in result["postings"]:
                positions += [int(position) for position in posting[3].split(",")]

            sorted_positions = sorted(positions)

            tokenized_site = open('tokenized_pages/' + site + '.txt', mode='r', encoding="utf8")

            tokens = []

            for line in tokenized_site:
                tokens.append(line.strip())

            shown_snippets = 0
            max_shown_snippets = 5

            for position in sorted_positions:
                # print("Position", position, tokens[position])

                if shown_snippets == max_shown_snippets:
                    pass
                else:
                    if snippets != "":
                        snippets += " ... "

                    words_radius = 3

                    starting_index = position - words_radius
                    ending_index = position + words_radius

                    if starting_index < 0:
                        starting_index = 0
                        ending_index += starting_index

                    if ending_index > len(tokens) - 1:
                        starting_index = 2*len(tokens) - 2 - ending_index

                        ending_index = len(tokens) - 1

                    for pos in range(starting_index, ending_index):
                        found_token = tokens[pos].strip()

                        if found_token == "." or found_token == ",":
                            snippets += tokens[pos].strip()
                        else:
                            snippets += " " + tokens[pos].strip()

                    shown_snippets += 1

            result["snippets"] = snippets.strip()

    def print_output(self, query, time_difference, results):
        print("[SEARCH WITH INVERTED INDEX] Results for a query: \"{}\"\n".format(query))

        print("     Results found in {:.0f}ms\n".format(time_difference.total_seconds() * 1000))

        print("     {:15s}{:40}{:60s}".format("Frequencies", "Document", "Snippet"))
        print("     {:15s}{:40}{:60s}".format("-" * 14, "-" * 39, "-" * 59))

        for result in results:
            print("     {:<15d}{:40}{}".format(result["total_frequencies"], result["site"], result["snippets"]))

        print("\n\n")
