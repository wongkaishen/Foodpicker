"""
Google Places API Restaurant Categories Discovery Tool

This script helps you discover all the restaurant categories and types 
that Google Places API can return for food establishments.
"""

import requests
import json
from collections import defaultdict
import os

# Your Google Maps API key
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def discover_restaurant_categories(location="Kuala Lumpur, Malaysia", radius=50000):
    """
    Discover all restaurant categories available in Google Places API
    by searching for food establishments in a given location.
    """
    
    # First, geocode the location
    geocoding_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geocoding_params = {
        'address': location,
        'key': API_KEY
    }
    
    geo_response = requests.get(geocoding_url, params=geocoding_params)
    geo_data = geo_response.json()
    
    if geo_data['status'] != 'OK':
        print(f"Geocoding failed: {geo_data['status']}")
        return
    
    location_coords = geo_data['results'][0]['geometry']['location']
    lat, lng = location_coords['lat'], location_coords['lng']
    
    print(f"Searching for restaurant categories near {location}")
    print(f"Coordinates: {lat}, {lng}")
    print("-" * 60)
    
    # Search strategies to find all types of food establishments
    search_strategies = [
        # By type
        {'type': 'restaurant'},
        {'type': 'food'},
        {'type': 'cafe'},
        {'type': 'bakery'},
        {'type': 'bar'},
        {'type': 'meal_takeaway'},
        {'type': 'meal_delivery'},
        
        # By keyword
        {'keyword': 'restaurant'},
        {'keyword': 'food'},
        {'keyword': 'cafe'},
        {'keyword': 'dining'},
        {'keyword': 'eatery'},
        {'keyword': 'fast food'},
        {'keyword': 'takeaway'},
        {'keyword': 'delivery'},
        {'keyword': 'pizza'},
        {'keyword': 'burger'},
        {'keyword': 'coffee'},
        {'keyword': 'tea'},
        {'keyword': 'ice cream'},
        {'keyword': 'bakery'},
        {'keyword': 'deli'},
        {'keyword': 'buffet'},
        {'keyword': 'fine dining'},
        {'keyword': 'casual dining'},
        {'keyword': 'seafood'},
        {'keyword': 'steakhouse'},
        {'keyword': 'sushi'},
        {'keyword': 'chinese'},
        {'keyword': 'indian'},
        {'keyword': 'italian'},
        {'keyword': 'mexican'},
        {'keyword': 'thai'},
        {'keyword': 'japanese'},
        {'keyword': 'korean'},
        {'keyword': 'vietnamese'},
        {'keyword': 'french'},
        {'keyword': 'mediterranean'},
        {'keyword': 'middle eastern'},
        {'keyword': 'halal'},
        {'keyword': 'vegetarian'},
        {'keyword': 'vegan'},
    ]
    
    all_types = set()
    all_places = []
    
    # Google Places API endpoint
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    for i, strategy in enumerate(search_strategies):
        print(f"Strategy {i+1}/{len(search_strategies)}: {strategy}")
        
        params = {
            'location': f"{lat},{lng}",
            'radius': radius,
            'key': API_KEY
        }
        params.update(strategy)
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'OK':
                results = data.get('results', [])
                print(f"  Found {len(results)} places")
                
                for place in results:
                    place_types = place.get('types', [])
                    all_types.update(place_types)
                    all_places.append({
                        'name': place.get('name'),
                        'types': place_types,
                        'price_level': place.get('price_level'),
                        'rating': place.get('rating'),
                        'business_status': place.get('business_status')
                    })
            else:
                print(f"  Error: {data.get('status')}")
                
        except requests.RequestException as e:
            print(f"  Request failed: {e}")
    
    print(f"\nTotal unique place types found: {len(all_types)}")
    print("-" * 60)
    
    # Categorize the types
    categorize_place_types(all_types)
    
    # Analyze places by types
    analyze_places_by_types(all_places)
    
    return all_types, all_places

def categorize_place_types(all_types):
    """Categorize the found place types into meaningful groups."""
    
    # Define category groups
    categories = {
        'Food Establishments': [
            'restaurant', 'food', 'establishment', 'meal_takeaway', 'meal_delivery'
        ],
        'Specific Restaurant Types': [
            'chinese_restaurant', 'japanese_restaurant', 'korean_restaurant',
            'thai_restaurant', 'vietnamese_restaurant', 'indian_restaurant',
            'italian_restaurant', 'mexican_restaurant', 'american_restaurant',
            'french_restaurant', 'mediterranean_restaurant', 'middle_eastern_restaurant',
            'seafood_restaurant', 'steak_house', 'hamburger_restaurant',
            'pizza_restaurant', 'sandwich_shop', 'sushi_restaurant',
            'ramen_restaurant', 'noodle_house', 'buffet_restaurant',
            'fine_dining_restaurant', 'family_restaurant', 'fast_food_restaurant',
            'brunch_restaurant', 'breakfast_restaurant'
        ],
        'Cafes & Coffee': [
            'cafe', 'coffee_shop', 'tea_house', 'espresso_bar'
        ],
        'Bars & Nightlife': [
            'bar', 'night_club', 'pub', 'wine_bar', 'cocktail_lounge',
            'sports_bar', 'dive_bar', 'rooftop_bar'
        ],
        'Bakeries & Desserts': [
            'bakery', 'pastry_shop', 'ice_cream_shop', 'frozen_yogurt_shop',
            'donut_shop', 'cupcake_shop', 'candy_store', 'chocolate_shop'
        ],
        'Quick Service': [
            'fast_food_restaurant', 'food_truck', 'street_vendor',
            'juice_bar', 'smoothie_bar', 'snack_bar'
        ],
        'Specialty Food': [
            'deli', 'delicatessen', 'grocery_store', 'supermarket',
            'butcher_shop', 'fish_market', 'farmers_market'
        ]
    }
    
    print("CATEGORIZED PLACE TYPES:")
    print("=" * 60)
    
    found_in_category = set()
    
    for category, types in categories.items():
        found_types = [t for t in types if t in all_types]
        if found_types:
            print(f"\n{category}:")
            for t in found_types:
                print(f"  - {t}")
                found_in_category.add(t)
    
    # Show uncategorized types
    uncategorized = all_types - found_in_category
    if uncategorized:
        print(f"\nUncategorized Types:")
        for t in sorted(uncategorized):
            print(f"  - {t}")

def analyze_places_by_types(all_places):
    """Analyze places by their types to understand patterns."""
    
    type_counts = defaultdict(int)
    type_examples = defaultdict(list)
    
    for place in all_places:
        for place_type in place['types']:
            type_counts[place_type] += 1
            if len(type_examples[place_type]) < 3:  # Keep first 3 examples
                type_examples[place_type].append(place['name'])
    
    print(f"\nTYPE FREQUENCY ANALYSIS:")
    print("=" * 60)
    
    # Sort by frequency
    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Show top 20 most common types
    print("Top 20 Most Common Place Types:")
    for i, (place_type, count) in enumerate(sorted_types[:20]):
        examples = ", ".join(type_examples[place_type][:2])
        print(f"{i+1:2d}. {place_type:<25} ({count:3d} places) - e.g., {examples}")

def get_google_restaurant_categories():
    """
    Returns the comprehensive list of Google Places API restaurant categories
    based on official documentation and real-world findings.
    """
    
    categories = {
        # Primary food establishment types
        'primary_types': [
            'restaurant',
            'food',
            'establishment',
            'meal_takeaway',
            'meal_delivery'
        ],
        
        # Cuisine-specific restaurants
        'cuisine_restaurants': [
            'american_restaurant',
            'chinese_restaurant',
            'french_restaurant',
            'greek_restaurant',
            'indian_restaurant',
            'italian_restaurant',
            'japanese_restaurant',
            'korean_restaurant',
            'mediterranean_restaurant',
            'mexican_restaurant',
            'middle_eastern_restaurant',
            'seafood_restaurant',
            'thai_restaurant',
            'vietnamese_restaurant'
        ],
        
        # Restaurant styles
        'restaurant_styles': [
            'fine_dining_restaurant',
            'fast_food_restaurant',
            'family_restaurant',
            'buffet_restaurant',
            'brunch_restaurant',
            'breakfast_restaurant',
            'hamburger_restaurant',
            'pizza_restaurant',
            'sandwich_shop',
            'steak_house',
            'sushi_restaurant',
            'ramen_restaurant',
            'noodle_house'
        ],
        
        # Cafes and coffee
        'cafes_coffee': [
            'cafe',
            'coffee_shop',
            'tea_house',
            'espresso_bar'
        ],
        
        # Bars and nightlife
        'bars_nightlife': [
            'bar',
            'night_club',
            'pub',
            'wine_bar',
            'cocktail_lounge',
            'sports_bar'
        ],
        
        # Bakeries and sweets
        'bakeries_sweets': [
            'bakery',
            'pastry_shop',
            'ice_cream_shop',
            'frozen_yogurt_shop',
            'donut_shop',
            'candy_store'
        ],
        
        # Quick service
        'quick_service': [
            'food_truck',
            'juice_bar',
            'smoothie_bar',
            'snack_bar'
        ],
        
        # Specialty food
        'specialty_food': [
            'deli',
            'delicatessen'
        ]
    }
    
    return categories

if __name__ == "__main__":
    print("Google Places API Restaurant Categories Discovery")
    print("=" * 60)
    
    # Discover categories in Kuala Lumpur (you can change this)
    all_types, all_places = discover_restaurant_categories("Kuala Lumpur, Malaysia")
    
    print(f"\n\nCOMPREHENSIVE RESTAURANT CATEGORIES:")
    print("=" * 60)
    
    # Show the comprehensive categorization
    categories = get_google_restaurant_categories()
    
    for category_name, types in categories.items():
        print(f"\n{category_name.replace('_', ' ').title()}:")
        for t in types:
            print(f"  - {t}")
    
    # Save results to a file
    results = {
        'discovered_types': list(all_types),
        'categorized_types': categories,
        'sample_places': all_places[:50]  # First 50 places as examples
    }
    
    with open('google_places_restaurant_categories.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n\nResults saved to 'google_places_restaurant_categories.json'")
    print(f"Total unique place types discovered: {len(all_types)}")
