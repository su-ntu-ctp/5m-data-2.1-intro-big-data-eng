"""
Test file for MongoDB Query - Question 2
Group by rated and count movies
"""
import pytest
import pymongo
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


try:
    from my_solution_q2 import group_by_rated
except ImportError:
    import sys
    sys.path.insert(0, '.')
    from my_solution_q2 import group_by_rated


@pytest.fixture(scope="module")
def movies_collection():
    """Connect to MongoDB and return the movies collection"""
    import dotenv
    dotenv.load_dotenv()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        pytest.skip("MONGODB_URI environment variable not set.")
        exit(1)
    DATABASE_NAME = "sample_mflix"

    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client[DATABASE_NAME]
    collection = db["movies"]
    
    count = collection.count_documents({})
    if count == 0:
        pytest.skip("Movies collection is empty.")
    
    yield collection
    client.close()


def test_function_exists():
    """Test that the group_by_rated function is defined"""
    assert callable(group_by_rated), "group_by_rated function should be defined"


def test_returns_list(movies_collection):
    """Test that function returns a list"""
    results = group_by_rated(movies_collection)
    assert isinstance(results, list), f"Function should return a list, got {type(results)}"


def test_returns_results(movies_collection):
    """Test that function returns results"""
    results = group_by_rated(movies_collection)
    assert len(results) > 0, "Function should return at least one rating group"


def test_result_structure(movies_collection):
    """Test that each result has correct structure"""
    results = group_by_rated(movies_collection)
    
    for result in results:
        assert isinstance(result, dict), "Each result should be a dictionary"
        assert '_id' in result, "Each result should have '_id' field (the rating)"
        assert 'movie_count' in result, "Each result should have 'movie_count' field"
        assert isinstance(result['movie_count'], int), "movie_count should be an integer"


def test_counts_are_positive(movies_collection):
    """Test that all counts are positive"""
    results = group_by_rated(movies_collection)
    
    for result in results:
        assert result['movie_count'] > 0, f"Count for rating '{result['_id']}' should be positive"


def test_total_count_matches(movies_collection):
    """Test that sum of all counts equals total movies (including those without rated field)"""
    results = group_by_rated(movies_collection)
    
    total_from_aggregation = sum(r['movie_count'] for r in results)
    
    # Total should equal ALL movies in collection
    # because $group includes documents with null/missing rated field as a group with _id: null
    total_movies = movies_collection.count_documents({})
    
    assert total_from_aggregation == total_movies, \
        f"Sum of counts ({total_from_aggregation}) should equal total movies ({total_movies}). " \
        f"Note: $group includes documents with null/missing 'rated' as a group with _id: null"


def test_compare_with_correct_implementation(movies_collection):
    """Test by comparing with correct implementation"""
    student_results = group_by_rated(movies_collection)
    
    # Correct implementation
    stage_group_rated = {
        "$group": {
            "_id": "$rated",
            "movie_count": {"$sum": 1},
        }
    }
    
    pipeline = [stage_group_rated]
    correct_results = list(movies_collection.aggregate(pipeline))
    
    # Convert to dictionaries for comparison
    student_dict = {r['_id']: r['movie_count'] for r in student_results}
    correct_dict = {r['_id']: r['movie_count'] for r in correct_results}
    
    assert len(student_dict) == len(correct_dict), \
        f"Should have {len(correct_dict)} rating groups, got {len(student_dict)}"
    
    for rating, count in correct_dict.items():
        assert rating in student_dict, f"Missing rating: {rating}"
        assert student_dict[rating] == count, \
            f"Count mismatch for rating '{rating}': expected {count}, got {student_dict[rating]}"


def test_includes_common_ratings(movies_collection):
    """Test that results include common movie ratings"""
    results = group_by_rated(movies_collection)
    ratings = {r['_id'] for r in results}
    
    # Common ratings that should exist in sample_mflix
    common_ratings = {'G', 'PG', 'PG-13', 'R'}
    found_ratings = ratings.intersection(common_ratings)
    
    assert len(found_ratings) > 0, \
        f"Should find at least one common rating (G, PG, PG-13, R), found: {ratings}"