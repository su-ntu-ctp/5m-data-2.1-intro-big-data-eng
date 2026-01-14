"""
Test suite for MongoDB assignment
All three questions in one file using classes
Can be imported into notebook or run with pytest
"""
import pymongo
from datetime import datetime


# ============================================================================
# Question 1: War Movies Query Tests
# ============================================================================
class TestQuestion1:
    """Tests for Question 1: Movies with plots starting with 'war'"""
    
    @staticmethod
    def test_function_exists(func):
        """Test that the function is defined"""
        assert callable(func), "Function should be defined and callable"
        return True
    
    @staticmethod
    def test_returns_list(func, movies_collection):
        """Test that function returns a list"""
        results = func(movies_collection)
        assert isinstance(results, list), f"Function should return a list, got {type(results)}"
        return True
    
    @staticmethod
    def test_returns_5_or_fewer_results(func, movies_collection):
        """Test that results are limited to 5 documents"""
        results = func(movies_collection)
        assert len(results) <= 5, f"Should return at most 5 results, got {len(results)}"
        assert len(results) > 0, "Should return at least 1 result"
        return True
    
    @staticmethod
    def test_correct_fields_returned(func, movies_collection):
        """Test that returned documents contain only title, plot, and released fields"""
        results = func(movies_collection)
        
        required_fields = {'title', 'plot', 'released'}
        
        for i, result in enumerate(results):
            result_fields = set(result.keys())
            assert result_fields == required_fields, \
                f"Result {i+1} should have fields {required_fields}, got {result_fields}"
        return True
    
    @staticmethod
    def test_plots_start_with_war(func, movies_collection):
        """Test that all returned plots start with 'war' (case-insensitive)"""
        results = func(movies_collection)
        
        for i, result in enumerate(results):
            plot = result.get('plot', '')
            assert plot.lower().startswith('war'), \
                f"Result {i+1}: Plot should start with 'war', got: '{plot[:50]}...'"
        return True
    
    @staticmethod
    def test_sorted_by_released_ascending(func, movies_collection):
        """Test that results are sorted by released date in ascending order"""
        results = func(movies_collection)
        
        dates = [r['released'] for r in results if r.get('released') is not None]
        
        for i in range(len(dates) - 1):
            assert dates[i] <= dates[i + 1], \
                f"Results should be sorted in ascending order. " \
                f"Date at position {i} ({dates[i]}) is after date at position {i+1} ({dates[i+1]})"
        return True
    
    @staticmethod
    def test_no_non_war_plots(func, movies_collection):
        """Test that no results have plots that don't start with 'war'"""
        results = func(movies_collection)
        
        for result in results:
            plot = result.get('plot', '')
            assert plot.lower().startswith('war'), \
                f"Found plot that doesn't start with 'war': '{plot[:100]}'"
        return True
    
    @staticmethod
    def test_compare_with_correct_query(func, movies_collection):
        """Test by comparing with the correct query implementation"""
        student_results = func(movies_collection)
        
        correct_results = []
        for m in movies_collection.find(
            {"plot": {"$regex": "^war", "$options": "i"}}
        ).sort('released', pymongo.ASCENDING).limit(5):
            correct_results.append({
                'title': m['title'],
                'plot': m['plot'],
                'released': m['released']
            })
        
        assert len(student_results) == len(correct_results), \
            f"Should return {len(correct_results)} results, got {len(student_results)}"
        
        for i, (student, correct) in enumerate(zip(student_results, correct_results)):
            assert student['title'] == correct['title'], \
                f"Result {i+1}: Title mismatch. Expected '{correct['title']}', got '{student['title']}'"
            assert student['released'] == correct['released'], \
                f"Result {i+1}: Released date mismatch for '{student['title']}'"
        return True
    
    @classmethod
    def run_all_tests(cls, func, movies_collection):
        """Run all tests for Question 1"""
        tests = [
            ("Function exists", cls.test_function_exists, [func]),
            ("Returns list", cls.test_returns_list, [func, movies_collection]),
            ("Returns 5 or fewer results", cls.test_returns_5_or_fewer_results, [func, movies_collection]),
            ("Correct fields returned", cls.test_correct_fields_returned, [func, movies_collection]),
            ("Plots start with 'war'", cls.test_plots_start_with_war, [func, movies_collection]),
            ("Sorted by released (ascending)", cls.test_sorted_by_released_ascending, [func, movies_collection]),
            ("No non-war plots", cls.test_no_non_war_plots, [func, movies_collection]),
            ("Compare with correct query", cls.test_compare_with_correct_query, [func, movies_collection]),
        ]
        
        return _run_tests("QUESTION 1: War Movies Query", tests)


# ============================================================================
# Question 2: Group by Rated Tests
# ============================================================================
class TestQuestion2:
    """Tests for Question 2: Group by rated and count"""
    
    @staticmethod
    def test_function_exists(func):
        """Test that the function is defined"""
        assert callable(func), "Function should be defined and callable"
        return True
    
    @staticmethod
    def test_returns_list(func, movies_collection):
        """Test that function returns a list"""
        results = func(movies_collection)
        assert isinstance(results, list), f"Function should return a list, got {type(results)}"
        return True
    
    @staticmethod
    def test_returns_results(func, movies_collection):
        """Test that function returns results"""
        results = func(movies_collection)
        assert len(results) > 0, "Function should return at least one rating group"
        return True
    
    @staticmethod
    def test_result_structure(func, movies_collection):
        """Test that each result has correct structure"""
        results = func(movies_collection)
        
        for result in results:
            assert isinstance(result, dict), "Each result should be a dictionary"
            assert '_id' in result, "Each result should have '_id' field (the rating)"
            assert 'movie_count' in result, "Each result should have 'movie_count' field"
            assert isinstance(result['movie_count'], int), "movie_count should be an integer"
        return True
    
    @staticmethod
    def test_counts_are_positive(func, movies_collection):
        """Test that all counts are positive"""
        results = func(movies_collection)
        
        for result in results:
            assert result['movie_count'] > 0, f"Count for rating '{result['_id']}' should be positive"
        return True
    
    @staticmethod
    def test_total_count_matches(func, movies_collection):
        """Test that sum of all counts equals total movies"""
        results = func(movies_collection)
        
        total_from_aggregation = sum(r['movie_count'] for r in results)
        total_movies = movies_collection.count_documents({})
        
        assert total_from_aggregation == total_movies, \
            f"Sum of counts ({total_from_aggregation}) should equal total movies ({total_movies}). " \
            f"MongoDB $group includes documents with null/missing 'rated' as a group with _id: null"
        return True
    
    @staticmethod
    def test_includes_common_ratings(func, movies_collection):
        """Test that results include common movie ratings"""
        results = func(movies_collection)
        ratings = {r['_id'] for r in results if r['_id'] is not None}
        
        common_ratings = {'G', 'PG', 'PG-13', 'R'}
        found_ratings = ratings.intersection(common_ratings)
        
        assert len(found_ratings) > 0, \
            f"Should find at least one common rating (G, PG, PG-13, R), found: {ratings}"
        return True
    
    @staticmethod
    def test_compare_with_correct_implementation(func, movies_collection):
        """Test by comparing with correct implementation"""
        student_results = func(movies_collection)
        
        stage_group_rated = {
            "$group": {
                "_id": "$rated",
                "movie_count": {"$sum": 1},
            }
        }
        
        pipeline = [stage_group_rated]
        correct_results = list(movies_collection.aggregate(pipeline))
        
        student_dict = {r['_id']: r['movie_count'] for r in student_results}
        correct_dict = {r['_id']: r['movie_count'] for r in correct_results}
        
        assert len(student_dict) == len(correct_dict), \
            f"Should have {len(correct_dict)} rating groups, got {len(student_dict)}"
        
        for rating, count in correct_dict.items():
            assert rating in student_dict, f"Missing rating: {rating}"
            assert student_dict[rating] == count, \
                f"Count mismatch for rating '{rating}': expected {count}, got {student_dict[rating]}"
        return True
    
    @classmethod
    def run_all_tests(cls, func, movies_collection):
        """Run all tests for Question 2"""
        tests = [
            ("Function exists", cls.test_function_exists, [func]),
            ("Returns list", cls.test_returns_list, [func, movies_collection]),
            ("Returns results", cls.test_returns_results, [func, movies_collection]),
            ("Result structure", cls.test_result_structure, [func, movies_collection]),
            ("Counts are positive", cls.test_counts_are_positive, [func, movies_collection]),
            ("Total count matches", cls.test_total_count_matches, [func, movies_collection]),
            ("Includes common ratings", cls.test_includes_common_ratings, [func, movies_collection]),
            ("Compare with correct implementation", cls.test_compare_with_correct_implementation, [func, movies_collection]),
        ]
        
        return _run_tests("QUESTION 2: Group by Rated", tests)


# ============================================================================
# Question 3: Count Movies with Comments Tests
# ============================================================================
class TestQuestion3:
    """Tests for Question 3: Count movies with 3+ comments"""
    
    @staticmethod
    def test_function_exists(func):
        """Test that the function is defined"""
        assert callable(func), "Function should be defined and callable"
        return True
    
    @staticmethod
    def test_returns_integer(func, movies_collection):
        """Test that function returns an integer"""
        result = func(movies_collection)
        assert isinstance(result, int), f"Function should return an integer, got {type(result)}"
        return True
    
    @staticmethod
    def test_returns_positive_count(func, movies_collection):
        """Test that function returns a positive count"""
        result = func(movies_collection)
        assert result > 0, "Should return at least 1 movie with 3+ comments in sample dataset"
        return True
    
    @staticmethod
    def test_count_is_reasonable(func, movies_collection):
        """Test that count is within reasonable range"""
        result = func(movies_collection)
        total_movies = movies_collection.count_documents({})
        
        assert result <= total_movies, \
            f"Count ({result}) cannot exceed total movies ({total_movies})"
        assert result > 0, "Count should be greater than 0"
        return True
    
    @staticmethod
    def test_compare_with_correct_query(func, movies_collection):
        """Test by comparing with correct query implementation"""
        student_count = func(movies_collection)
        correct_count = movies_collection.count_documents({"num_mflix_comments": {"$gte": 3}})
        
        assert student_count == correct_count, \
            f"Count mismatch: expected {correct_count}, got {student_count}"
        return True
    
    @staticmethod
    def test_boundary_case_exactly_3_comments(func, movies_collection):
        """Test that movies with exactly 3 comments are included"""
        student_count = func(movies_collection)
        
        exactly_3 = movies_collection.count_documents({"num_mflix_comments": 3})
        more_than_3 = movies_collection.count_documents({"num_mflix_comments": {"$gt": 3}})
        expected_count = exactly_3 + more_than_3
        
        assert student_count == expected_count, \
            f"Should include movies with exactly 3 comments. Expected {expected_count}, got {student_count}"
        return True
    
    @classmethod
    def run_all_tests(cls, func, movies_collection):
        """Run all tests for Question 3"""
        tests = [
            ("Function exists", cls.test_function_exists, [func]),
            ("Returns integer", cls.test_returns_integer, [func, movies_collection]),
            ("Returns positive count", cls.test_returns_positive_count, [func, movies_collection]),
            ("Count is reasonable", cls.test_count_is_reasonable, [func, movies_collection]),
            ("Compare with correct query", cls.test_compare_with_correct_query, [func, movies_collection]),
            ("Boundary case (exactly 3)", cls.test_boundary_case_exactly_3_comments, [func, movies_collection]),
        ]
        
        return _run_tests("QUESTION 3: Count Movies with 3+ Comments", tests)


# ============================================================================
# Helper Functions
# ============================================================================
def _run_tests(title, tests):
    """
    Helper function to run a list of tests
    Returns: (passed_count, failed_count, results)
    """
    results = []
    passed = 0
    failed = 0
    
    print("=" * 70)
    print(f"{title}")
    print("=" * 70)
    
    for test_name, test_func, args in tests:
        try:
            test_func(*args)
            print(f"✅ PASSED: {test_name}")
            results.append((test_name, "PASSED", None))
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {str(e)}")
            results.append((test_name, "FAILED", str(e)))
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {test_name}")
            print(f"   Error: {str(e)}")
            results.append((test_name, "ERROR", str(e)))
            failed += 1
    
    print("=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return passed, failed, results




