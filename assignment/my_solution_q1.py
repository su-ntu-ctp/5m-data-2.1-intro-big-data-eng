import pymongo

# Student's solution
def war_movies(movies_collection):
    """
    Enter Your Solution Here

    """
    results = []

    # Start your solutions
    for m in movies_collection.find({"plot": {"$regex": "^[Ww]ar"}}).sort('released', pymongo.ASCENDING).limit(5):
        results.append({
            'title': m['title'],
            'plot': m['plot'],
            'released': m['released']
        })
    # Your solution ends here
    
    return results
