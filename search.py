# search.py - Julian Zulfikar, 2023
# ------------------------------------------------------------------
# Shell implementation of the catalogue search.

from index import Index

from nltk.tokenize import wordpunct_tokenize

INDEX_OBJ = Index()
DATA_INDEX = INDEX_OBJ.get_index()
DATA_INVERTED_INDEX = INDEX_OBJ.get_inverted_index()


def query_catalogue(query: str) -> list[str]:
    """
    Queries the indexes and returns results sorted by TF-IDF.
    """
    # Tokenize/lemmatize
    course_to_score = {}
    tokens = [INDEX_OBJ._lemmatize_with_pos(token) for token in wordpunct_tokenize(query)]
    for token in tokens:
        if token in DATA_INVERTED_INDEX:
            for page in DATA_INVERTED_INDEX[token]:
                course_to_score[page[0]] = course_to_score.get(page[0], 0) + page[2]

    # Sort by TF-IDF
    sorted_results = sorted(course_to_score.keys(), key = lambda x:-course_to_score[x])
    
    return sorted_results


if __name__ == "__main__":    
    while True:
        # Prompt for query
        query = input("Query: ")
        print('-'*50)
        if query == "DONE":
            break

        # Query the index
        sorted_results = query_catalogue(query)

        # Print results
        for course in sorted_results:
            print(course, '-', DATA_INDEX[course][1])
            print(DATA_INDEX[course][2])
            print('-'*50)

