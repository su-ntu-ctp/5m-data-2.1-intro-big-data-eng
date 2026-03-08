# Assignment

## Brief

Write the Python codes for the following questions.

## Instructions

Paste the answer as Python in the answer code section below each question.

### Question 1

Question: From the `movies` collection, return the documents with the `plot` that starts with `"war"` in acending order of released date, print only title, plot and released fields. Limit the result to 5.

Answer:

```python
def war_movies(movies_collection):
    results = []
    
    # Start your solution
    cursor = movies_collection.find(
        {"plot": {"$regex": "^war", "$options": "i"}}  # plot starts with "war" (case insensitive)
    ).sort("released", pymongo.ASCENDING).limit(5)
    
    for movie in cursor:
        
        # Append only the required fields to results
        results.append({
            "title": movie["title"],
            "plot": movie["plot"],
            "released": movie["released"]
        })
    # Your solution ends here
    
    return results
```

### Question 2

Question: Group by `rated` and count the number of movies in each.

Answer:

```python
def group_by_rated(movies_collection):
    """
    Group by `rated` and count the number of movies in each.
    """
    results = []
    
    # Start your solution
    pipeline = [
        {
            "$group": {
                "_id": "$rated",                    # This becomes the _id field in results
                "movie_count": {"$sum": 1}           # This becomes movie_count field (not "count")
            }
        },
        {
            "$sort": {"movie_count": -1}             # Sort by movie_count descending
        }
    ]
    
    cursor = movies_collection.aggregate(pipeline)
    
    for doc in cursor:
        # The test expects each result to have '_id' and 'movie_count' fields
        results.append(doc)
        
    # End your solution
    
    return results
```

### Question 3

Question: Count the number of movies with 3 comments or more.

Answer:

```python
def count_movies_with_comments(movies_collection):
    """
    Count the number of movies with 3 comments or more.
    """
    count = 0
    
    # Start your solution
    # Query for movies where num_mflix_comments is greater than or equal to 3
    count = movies_collection.count_documents({
        "num_mflix_comments": {"$gte": 3}
    })
    
    # Alternative using find (if you need to see the movies):
    # cursor = movies_collection.find({"num_mflix_comments": {"$gte": 3}})
    # count = len(list(cursor))
    
    # End your solution
    
    return count
```

## Submission

- Submit the URL of the GitHub Repository that contains your work to NTU black board.
- Should you reference the work of your classmate(s) or online resources, give them credit by adding either the name of your classmate or URL.
