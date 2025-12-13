import pymongo

def group_by_rated(movies_collection):
    """
    Group by rated and count the number of movies in each.
    Returns a list of dictionaries with '_id' (rating) and 'movie_count'
    """
    results = []
    
    # Start your solution
    stage_group_rated = {
        "$group": {
            "_id": "$rated",
            "movie_count": {"$sum": 1},
        }
    }
    
    pipeline = [stage_group_rated]
    
    for result in movies_collection.aggregate(pipeline):
        results.append(result)
    # End your solution
    
    return results
