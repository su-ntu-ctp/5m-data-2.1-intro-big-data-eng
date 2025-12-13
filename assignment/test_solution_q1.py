"""
Test file for MongoDB query assignment
Tests against actual MongoDB sample_mflix dataset
"""
import pytest
import pymongo
import os
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Import learner solution
try:
    from my_solution_q1 import war_movies
except ImportError:
    # Fallback: try to import from notebook directly
    import sys
    sys.path.insert(0, '.')
    from my_solution_q1 import war_movies


@pytest.fixture(scope="module")
def movies_collection():
    """
    Connect to MongoDB and return the movies collection
    Uses the same connection as in the notebook
    """
    import dotenv
    dotenv.load_dotenv()

    uri = os.getenv("MONGODB_URI")
    if not uri:
        pytest.skip("MONGODB_URI environment variable not set.")
        exit(1)
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["sample_mflix"]
    collection = db["movies"]
    
    # Verify collection has data
    count = collection.count_documents({})
    if count == 0:
        pytest.skip("Movies collection is empty. Load sample_mflix dataset first.")
    
    yield collection
    
    # Cleanup
    client.close()


def test_function_exists():
    """Test that the query_war_movies function is defined"""
    assert callable(war_movies), "query_war_movies function should be defined"


def test_returns_list(movies_collection):
    """Test that function returns a list"""
    results = war_movies(movies_collection)
    assert isinstance(results, list), f"Function should return a list, got {type(results)}"


def test_returns_5_or_fewer_results(movies_collection):
    """Test that results are limited to 5 documents"""
    results = war_movies(movies_collection)
    assert len(results) <= 5, f"Should return at most 5 results, got {len(results)}"
    assert len(results) > 0, "Should return at least 1 result (sample dataset has movies with 'war' plots)"


def test_correct_fields_returned(movies_collection):
    """Test that returned documents contain only title, plot, and released fields"""
    results = war_movies(movies_collection)
    
    required_fields = {'title', 'plot', 'released'}
    
    for i, result in enumerate(results):
        result_fields = set(result.keys())
        assert result_fields == required_fields, \
            f"Result {i+1} should have fields {required_fields}, got {result_fields}"


def test_plots_start_with_war(movies_collection):
    """Test that all returned plots start with 'war' (case-insensitive)"""
    results = war_movies(movies_collection)
    
    for i, result in enumerate(results):
        plot = result.get('plot', '')
        assert plot.lower().startswith('war'), \
            f"Result {i+1}: Plot should start with 'war', got: '{plot[:50]}...'"


def test_sorted_by_released_ascending(movies_collection):
    """Test that results are sorted by released date in ascending order"""
    results = war_movies(movies_collection)
    
    # Extract released dates
    dates = [r['released'] for r in results if r.get('released') is not None]
    
    # Check if sorted in ascending order
    for i in range(len(dates) - 1):
        assert dates[i] <= dates[i + 1], \
            f"Results should be sorted in ascending order. " \
            f"Date at position {i} ({dates[i]}) is after date at position {i+1} ({dates[i+1]})"


def test_no_non_war_plots(movies_collection):
    """Test that no results have plots that don't start with 'war'"""
    results = war_movies(movies_collection)
    
    for result in results:
        plot = result.get('plot', '')
        # Should NOT match plots with 'war' in the middle
        # e.g., "A story about warfare" should NOT be included
        assert plot.lower().startswith('war'), \
            f"Found plot that doesn't start with 'war': '{plot[:100]}'"


def test_compare_with_correct_query(movies_collection):
    """Test by comparing with the correct query implementation"""
    student_results = war_movies(movies_collection)
    
    # Correct query
    correct_results = []
    for m in movies_collection.find(
        {"plot": {"$regex": "^war", "$options": "i"}}
    ).sort('released', pymongo.ASCENDING).limit(5):
        correct_results.append({
            'title': m['title'],
            'plot': m['plot'],
            'released': m['released']
        })
    
    # Compare counts
    assert len(student_results) == len(correct_results), \
        f"Should return {len(correct_results)} results, got {len(student_results)}"
    
    # Compare actual results (should be identical)
    for i, (student, correct) in enumerate(zip(student_results, correct_results)):
        assert student['title'] == correct['title'], \
            f"Result {i+1}: Title mismatch. Expected '{correct['title']}', got '{student['title']}'"
        assert student['released'] == correct['released'], \
            f"Result {i+1}: Released date mismatch for '{student['title']}'"