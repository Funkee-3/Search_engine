from wiki import article_metadata, ask_search, ask_advanced_search

# FOR ALL OF THESE FUNCTIONS, READ THE FULL INSTRUCTIONS.

# 1) 
#
# Function: search
#
# Parameters:
#   keyword - search word to look for in article metadata's relevant keywords
#
# Returns: list of metadata for articles in which the article is relevant to
#   the keyword. Relevance is determined by checking the metadata's "relevant
#   keywords" list for a case-insensitive match with the keyword parameter. #   The returned list should not include the "relevant keywords" list for each
#   article metadata.
#   
#   If the user does not enter anything, return an empty list
#
# Hint: to get list of existing article metadata, use article_metadata()
metadata_list = article_metadata()

def search(keyword):
    if keyword == '':
        return []
    keyword = keyword.strip().lower()
    result = []
    for metadata in metadata_list:
        for key in metadata[4]:
            relevant_keywords = key.lower()
            if keyword == relevant_keywords:
                result.append(metadata[:4])  #excluding the relevant keywords
    return result

# 2) 
#
# Function: article_length
#
# Parameters:
#   max_length - max character length of articles
#   metadata - article metadata to search through
#
# Returns: list of article metadata from given metadata with articles not
#   exceeding max_length number of characters
def article_length(max_length, metadata):
    result = []
    for data in metadata:
        if data[3] <= max_length:
            result.append(data[:4])  # also excluding the keywords according to the example given 
    return result

# 3) 
#
# Function: unique_authors
#
# Parameters:
#   count - max number of unique authors to include in the results
#   metadata - article metadata
#
# Returns: list of article metadata containing a maximum of `count` results,
#   each with a unique author. If two or more articles have the same author, 
#   include the first in the results and skip the others. Two authors are 
#   considered the same if they are a case-insensitive match. If count is 
#   larger than the number of unique authors, return all articles with the 
#   duplicate authors removed.
def unique_authors(count, metadata):
    if count <= 0:
        return []
    result = []
    picked_authors = set()
    for data in metadata:
        author = data[1].lower()
        
        if author not in picked_authors:
            result.append(data)
            picked_authors.add(author)
        
        if len(result) == count: #if we have reached the inputted count of unique authors
            break
    return result

# 4) 
#
# Function: most_recent_article
#
# Parameters:
#   metadata - article metadata
#
# Returns: article metadata of the article published most recently according
#   to the timestamp. Note this should return just a 1D list representing
#   a single article.
def most_recent_article(metadata):
    if not metadata:
        return []
    most_recent = metadata[0]
    
    for article in metadata[1:]: #to check the rest of the articles
        if article[2] > most_recent[2]:
            most_recent = article
    return most_recent



# 5) 
#
# Function: favorite_author
#
# Parameters:
#   favorite - favorite author title
#   metadata - article metadata
#
# Returns: True if favorite author is in the given articles (case 
#   insensitive), False otherwise
def favorite_author(favorite, metadata):
    result = []
    for article in metadata:
        if article[1].lower() == favorite.lower():
            return True
    return False

# 6) 
#
# Function: title_and_author
#
# Parameters:
#   metadata - article metadata
#
# Returns: list of Tuples containing (title, author) for all of the given 
#   metadata.
def title_and_author(metadata):
    result = []
    for data in metadata:
        title_and_author_tuple = (data[0], data[1])
        result.append(title_and_author_tuple)
    return result
    

# 7) 
#
# Function: refine_search
#
# Parameters:
#   keyword - additional keyword to search
#   metadata - article metadata from basic search
#
# Returns: searches for article metadata from entire list of available
#   articles using keyword. Returns the article metadata that is returned in 
#   in *both* the additional search and the basic search. The results should
#   be in the same order that they were returned in the basic search. Two
#   articles can be considered the same if both their author and article title
#   match exactly.
def refine_search(keyword, metadata):
    results = search(keyword)

    matched_articles = []
    for article in metadata:
        for result in results:
            if article[0].lower() == result[0].lower() and article[1].lower() == result[1].lower():
                matched_articles.append(article)
                break 
                #goes to the next article
    return matched_articles



# Prints out articles based on searched keyword and advanced options
def display_result():
    # Stores list of articles returned from searching user's keyword
    articles = search(ask_search())

    # advanced stores user's chosen advanced option (1-7)
    # value stores user's response in being asked the advanced option
    advanced, value = ask_advanced_search()

    if advanced == 1:
        # value stores max article title length in number of characters
        # Update article metadata to contain only ones of the maximum length
        articles = article_length(value, articles)
    if advanced == 2:
        # value stores max number of unique authors
        # Update article metadata to contain only the max number of authors
        articles = unique_authors(value, articles)
    elif advanced == 3:
        # Update articles to only contain the most recent article
        articles = most_recent_article(articles)
    elif advanced == 4:
        # value stores author
        # Store whether author is in search results into variable named 
        # has_favorite
        has_favorite = favorite_author(value, articles)
    elif advanced == 5:
        # Update article metadata to only contain titles and authors
        articles = title_and_author(articles)
    elif advanced == 6:
        # value stores keyword to search
        # Update article metadata to contain only article metadata
        # that is contained in both searches
        articles = refine_search(value, articles)

    print()

    if not articles:
        print("No articles found")
    else:
        print("Here are your articles: " + str(articles))

    if advanced == 4:
        print("Your favorite author is" + ("" if has_favorite else " not") + " in the returned articles!")

if __name__ == "__main__":
    display_result()
