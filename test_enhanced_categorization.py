#!/usr/bin/env python3
"""
Test script to verify the enhanced Google Places categorization integration.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

# Import the enhanced categorization functions
from google_places_categories import categorize_google_place, get_comprehensive_search_strategies

def test_categorization():
    """Test the enhanced categorization with sample place data."""
    
    # Sample place data (similar to what Google Places API returns)
    test_places = [
        {
            'name': 'Pizza Palace',
            'types': ['restaurant', 'food', 'establishment'],
            'place_id': 'test_1'
        },
        {
            'name': 'Starbucks Coffee',
            'types': ['cafe', 'food', 'establishment'],
            'place_id': 'test_2'
        },
        {
            'name': 'Sushi Zen',
            'types': ['restaurant', 'food', 'establishment'],
            'place_id': 'test_3'
        },
        {
            'name': 'Local Bakery',
            'types': ['bakery', 'food', 'establishment'],
            'place_id': 'test_4'
        },
        {
            'name': 'Sports Bar & Grill',
            'types': ['bar', 'restaurant', 'food', 'establishment'],
            'place_id': 'test_5'
        }
    ]
    
    print("Testing Enhanced Google Places Categorization")
    print("=" * 50)
    
    for place in test_places:
        print(f"\nPlace: {place['name']}")
        print(f"Google Types: {place['types']}")
        
        result = categorize_google_place(place)
        
        print(f"Cuisine: {result['cuisine']}")
        print(f"Establishment: {result['establishment_type']}")
        print(f"Confidence: {result['confidence']:.2f}")
        print(f"Keywords Matched: {result['keywords_matched']}")
        print("-" * 30)

def test_search_strategies():
    """Test the comprehensive search strategies."""
    
    print("\nTesting Search Strategies")
    print("=" * 50)
    
    strategies = get_comprehensive_search_strategies()
    
    print(f"Total search strategies: {len(strategies)}")
    
    # Group by strategy type
    type_strategies = [s for s in strategies if 'type' in s]
    keyword_strategies = [s for s in strategies if 'keyword' in s]
    
    print(f"Type-based strategies: {len(type_strategies)}")
    print(f"Keyword-based strategies: {len(keyword_strategies)}")
    
    print("\nType-based strategies:")
    for strategy in type_strategies:
        print(f"  - {strategy['type']}")
    
    print(f"\nFirst 10 keyword strategies:")
    for strategy in keyword_strategies[:10]:
        print(f"  - {strategy['keyword']}")
    
    if len(keyword_strategies) > 10:
        print(f"  ... and {len(keyword_strategies) - 10} more")

if __name__ == "__main__":
    try:
        test_categorization()
        test_search_strategies()
        print("\n✅ All tests completed successfully!")
        print("The enhanced categorization system is ready for integration.")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        print("Please check the integration and try again.")
