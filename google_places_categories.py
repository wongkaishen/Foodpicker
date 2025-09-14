"""
Enhanced Google Places Restaurant Categories Module

This module provides comprehensive categorization and filtering
for Google Places API restaurant types and categories.
"""

def get_google_restaurant_categories():
    """
    Returns the comprehensive mapping of Google Places API restaurant categories
    organized by type for better filtering and display.
    """
    return {
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
        
        # Restaurant styles and formats
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
        
        # Cafes and coffee shops
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
            'sports_bar',
            'dive_bar',
            'rooftop_bar'
        ],
        
        # Bakeries and desserts
        'bakeries_sweets': [
            'bakery',
            'pastry_shop',
            'ice_cream_shop',
            'frozen_yogurt_shop',
            'donut_shop',
            'candy_store',
            'chocolate_shop',
            'cupcake_shop'
        ],
        
        # Quick service and street food
        'quick_service': [
            'food_truck',
            'juice_bar', 
            'smoothie_bar',
            'snack_bar',
            'street_vendor'
        ],
        
        # Specialty food stores
        'specialty_food': [
            'deli',
            'delicatessen',
            'butcher_shop',
            'fish_market'
        ]
    }

def get_enhanced_cuisine_mapping():
    """
    Enhanced cuisine mapping that includes Google Places API specific types
    and broader keyword matching for better categorization.
    """
    return {
        'AMERICAN': {
            'google_types': ['american_restaurant', 'hamburger_restaurant', 'steak_house'],
            'keywords': ['american', 'burger', 'hamburger', 'cheeseburger', 'steak', 'barbecue', 'bbq', 'grill', 'diner', 'usa', 'wings', 'ribs'],
            'display_name': 'American'
        },
        'CHINESE': {
            'google_types': ['chinese_restaurant'],
            'keywords': ['chinese', 'dim sum', 'szechuan', 'cantonese', 'mandarin', 'peking', 'beijing', 'shanghai', 'hong kong', 'wonton', 'dumpling', 'noodle chinese'],
            'display_name': 'Chinese'
        },
        'JAPANESE': {
            'google_types': ['japanese_restaurant', 'sushi_restaurant', 'ramen_restaurant'],
            'keywords': ['japanese', 'sushi', 'sashimi', 'ramen', 'udon', 'tempura', 'yakitori', 'hibachi', 'teriyaki', 'miso', 'sake', 'izakaya', 'bento'],
            'display_name': 'Japanese'
        },
        'KOREAN': {
            'google_types': ['korean_restaurant'],
            'keywords': ['korean', 'kimchi', 'bulgogi', 'bibimbap', 'galbi', 'seoul', 'bbq korean', 'kbbq', 'banchan'],
            'display_name': 'Korean'
        },
        'THAI': {
            'google_types': ['thai_restaurant'],
            'keywords': ['thai', 'pad thai', 'tom yum', 'green curry', 'red curry', 'massaman', 'bangkok', 'som tam', 'thai basil'],
            'display_name': 'Thai'
        },
        'VIETNAMESE': {
            'google_types': ['vietnamese_restaurant'],
            'keywords': ['vietnamese', 'pho', 'banh mi', 'spring roll', 'saigon', 'ho chi minh', 'vermicelli'],
            'display_name': 'Vietnamese'
        },
        'INDIAN': {
            'google_types': ['indian_restaurant'],
            'keywords': ['indian', 'curry', 'tandoori', 'biryani', 'naan', 'tikka', 'masala', 'dal', 'samosa', 'india', 'bollywood'],
            'display_name': 'Indian'
        },
        'ITALIAN': {
            'google_types': ['italian_restaurant', 'pizza_restaurant'],
            'keywords': ['italian', 'pizza', 'pasta', 'spaghetti', 'lasagna', 'risotto', 'gelato', 'trattoria', 'pizzeria', 'romano', 'tuscany', 'margherita'],
            'display_name': 'Italian'
        },
        'MEXICAN': {
            'google_types': ['mexican_restaurant'],
            'keywords': ['mexican', 'taco', 'burrito', 'quesadilla', 'nachos', 'salsa', 'guacamole', 'tortilla', 'enchilada', 'mexico', 'chipotle'],
            'display_name': 'Mexican'
        },
        'FRENCH': {
            'google_types': ['french_restaurant'],
            'keywords': ['french', 'bistro', 'brasserie', 'croissant', 'baguette', 'france', 'cafe french', 'crepe', 'coq au vin'],
            'display_name': 'French'
        },
        'MEDITERRANEAN': {
            'google_types': ['mediterranean_restaurant', 'middle_eastern_restaurant'],
            'keywords': ['mediterranean', 'middle eastern', 'lebanese', 'hummus', 'falafel', 'shawarma', 'pita', 'olive', 'tzatziki'],
            'display_name': 'Mediterranean'
        },
        'GREEK': {
            'google_types': ['greek_restaurant'],
            'keywords': ['greek', 'gyro', 'souvlaki', 'moussaka', 'feta', 'tzatziki', 'greece', 'mediterranean greek', 'spanakopita'],
            'display_name': 'Greek'
        },
        'SEAFOOD': {
            'google_types': ['seafood_restaurant'],
            'keywords': ['seafood', 'fish', 'lobster', 'crab', 'shrimp', 'oyster', 'salmon', 'tuna', 'sushi seafood', 'crab house'],
            'display_name': 'Seafood'
        },
        'FAST_FOOD': {
            'google_types': ['fast_food_restaurant', 'hamburger_restaurant'],
            'keywords': ['fast food', 'quick service', 'drive thru', 'mcdonald', 'burger king', 'kfc', 'subway', 'pizza hut', 'domino'],
            'display_name': 'Fast Food'
        },
        'CAFE': {
            'google_types': ['cafe', 'coffee_shop'],
            'keywords': ['cafe', 'coffee', 'espresso', 'cappuccino', 'latte', 'starbucks', 'costa', 'coffee bean', 'coffee shop'],
            'display_name': 'Cafe & Coffee'
        },
        'BAKERY': {
            'google_types': ['bakery', 'pastry_shop'],
            'keywords': ['bakery', 'pastry', 'bread', 'cake', 'donut', 'croissant', 'muffin', 'cupcake', 'danish'],
            'display_name': 'Bakery & Pastry'
        },
        'DESSERT': {
            'google_types': ['ice_cream_shop', 'frozen_yogurt_shop', 'candy_store'],
            'keywords': ['ice cream', 'gelato', 'frozen yogurt', 'sorbet', 'dessert', 'sweet', 'candy', 'chocolate'],
            'display_name': 'Desserts & Sweets'
        },
        'BAR': {
            'google_types': ['bar', 'wine_bar', 'cocktail_lounge', 'sports_bar'],
            'keywords': ['bar', 'pub', 'lounge', 'tavern', 'brewery', 'cocktail', 'wine bar', 'sports bar', 'rooftop bar'],
            'display_name': 'Bars & Pubs'
        },
        'FINE_DINING': {
            'google_types': ['fine_dining_restaurant'],
            'keywords': ['fine dining', 'upscale', 'gourmet', 'michelin', 'haute cuisine', 'tasting menu', 'chef table'],
            'display_name': 'Fine Dining'
        },
        'BUFFET': {
            'google_types': ['buffet_restaurant'],
            'keywords': ['buffet', 'all you can eat', 'smorgasbord', 'self service', 'unlimited'],
            'display_name': 'Buffet'
        },
        'HALAL': {
            'google_types': [],
            'keywords': ['halal', 'muslim', 'islamic', 'no pork', 'halal certified'],
            'display_name': 'Halal'
        },
        'VEGETARIAN': {
            'google_types': [],
            'keywords': ['vegetarian', 'veggie', 'plant based', 'meat free'],
            'display_name': 'Vegetarian'
        },
        'VEGAN': {
            'google_types': [],
            'keywords': ['vegan', 'plant based', 'dairy free', 'no animal products'],
            'display_name': 'Vegan'
        }
    }

def get_establishment_type_mapping():
    """
    Enhanced establishment type mapping for Google Places API.
    """
    return {
        'RESTAURANT': {
            'google_types': ['restaurant', 'fine_dining_restaurant', 'family_restaurant'],
            'keywords': ['restaurant', 'dining', 'eatery'],
            'display_name': 'Restaurant'
        },
        'FAST_FOOD': {
            'google_types': ['fast_food_restaurant'],
            'keywords': ['fast food', 'quick service', 'drive thru'],
            'display_name': 'Fast Food'
        },
        'CAFE': {
            'google_types': ['cafe', 'coffee_shop'],
            'keywords': ['cafe', 'coffee shop', 'coffee house'],
            'display_name': 'Cafe'
        },
        'BAR': {
            'google_types': ['bar', 'pub', 'wine_bar', 'sports_bar', 'cocktail_lounge'],
            'keywords': ['bar', 'pub', 'lounge', 'tavern', 'brewery'],
            'display_name': 'Bar/Pub'
        },
        'BAKERY': {
            'google_types': ['bakery', 'pastry_shop'],
            'keywords': ['bakery', 'pastry', 'bread shop'],
            'display_name': 'Bakery'
        },
        'TAKEAWAY': {
            'google_types': ['meal_takeaway', 'meal_delivery'],
            'keywords': ['takeaway', 'delivery', 'pickup', 'to go'],
            'display_name': 'Takeaway/Delivery'
        },
        'FOOD_TRUCK': {
            'google_types': ['food_truck'],
            'keywords': ['food truck', 'mobile kitchen', 'street food'],
            'display_name': 'Food Truck'
        },
        'ICE_CREAM': {
            'google_types': ['ice_cream_shop', 'frozen_yogurt_shop'],
            'keywords': ['ice cream', 'gelato', 'frozen yogurt'],
            'display_name': 'Ice Cream Shop'
        },
        'BUFFET': {
            'google_types': ['buffet_restaurant'],
            'keywords': ['buffet', 'all you can eat'],
            'display_name': 'Buffet'
        },
        'DELI': {
            'google_types': ['deli', 'delicatessen', 'sandwich_shop'],
            'keywords': ['deli', 'delicatessen', 'sandwich shop'],
            'display_name': 'Deli'
        }
    }

def categorize_google_place(place):
    """
    Enhanced categorization function that uses Google Places API data
    to categorize establishments.
    
    Args:
        place: Dict containing Google Places API place data with 'types', 'name', etc.
    
    Returns:
        dict: Contains cuisine, establishment_type, confidence, and keywords_matched
    """
    place_types = place.get('types', [])
    place_name = place.get('name', '')
    
    if not place_types:
        return {
            'cuisine': 'General',
            'establishment_type': 'Restaurant',
            'confidence': 0.0,
            'keywords_matched': []
        }
    
    place_types_lower = [pt.lower() for pt in place_types]
    search_text = ' '.join(place_types_lower + [place_name.lower() if place_name else ""])
    
    cuisine_mapping = get_enhanced_cuisine_mapping()
    establishment_mapping = get_establishment_type_mapping()
    
    # Find cuisine type
    cuisine_scores = {}
    keywords_matched = []
    
    for cuisine, config in cuisine_mapping.items():
        score = 0
        
        # Check Google types (high confidence)
        for google_type in config['google_types']:
            if google_type in place_types_lower:
                score += 10
                keywords_matched.append(google_type)
        
        # Check keywords (medium confidence)
        for keyword in config['keywords']:
            if keyword in search_text:
                score += 5
                keywords_matched.append(keyword)
        
        if score > 0:
            cuisine_scores[cuisine] = score
    
    # Find establishment type
    establishment_scores = {}
    for est_type, config in establishment_mapping.items():
        score = 0
        
        # Check Google types (high confidence)
        for google_type in config['google_types']:
            if google_type in place_types_lower:
                score += 10
        
        # Check keywords (medium confidence)
        for keyword in config['keywords']:
            if keyword in search_text:
                score += 5
        
        if score > 0:
            establishment_scores[est_type] = score
    
    # Determine best matches
    best_cuisine = max(cuisine_scores.items(), key=lambda x: x[1]) if cuisine_scores else ('General', 0)
    best_establishment = max(establishment_scores.items(), key=lambda x: x[1]) if establishment_scores else ('Restaurant', 0)
    
    return {
        'cuisine': best_cuisine[0],
        'establishment_type': best_establishment[0],
        'confidence': (best_cuisine[1] + best_establishment[1]) / 20.0,  # Normalized confidence score
        'keywords_matched': list(set(keywords_matched))  # Remove duplicates
    }

def get_search_strategies_for_categories():
    """
    Returns optimized search strategies for Google Places API
    to find different types of food establishments.
    """
    return {
        'comprehensive_search': [
            # Primary types
            {'type': 'restaurant'},
            {'type': 'food'}, 
            {'type': 'cafe'},
            {'type': 'bakery'},
            {'type': 'bar'},
            {'type': 'meal_takeaway'},
            {'type': 'meal_delivery'},
            
            # Specific restaurant types (if supported by API)
            {'keyword': 'chinese restaurant'},
            {'keyword': 'japanese restaurant'},
            {'keyword': 'italian restaurant'},
            {'keyword': 'indian restaurant'},
            {'keyword': 'thai restaurant'},
            {'keyword': 'korean restaurant'},
            {'keyword': 'vietnamese restaurant'},
            {'keyword': 'mexican restaurant'},
            {'keyword': 'american restaurant'},
            {'keyword': 'french restaurant'},
            {'keyword': 'mediterranean restaurant'},
            {'keyword': 'seafood restaurant'},
            
            # Establishment styles
            {'keyword': 'fast food'},
            {'keyword': 'fine dining'},
            {'keyword': 'buffet restaurant'},
            {'keyword': 'pizza'},
            {'keyword': 'burger'},
            {'keyword': 'sushi'},
            {'keyword': 'steakhouse'},
            {'keyword': 'coffee shop'},
            {'keyword': 'ice cream'},
            {'keyword': 'bakery'},
            {'keyword': 'deli'},
            
            # Special dietary
            {'keyword': 'halal restaurant'},
            {'keyword': 'vegetarian restaurant'},
            {'keyword': 'vegan restaurant'},
        ],
        
        'quick_search': [
            {'type': 'restaurant'},
            {'type': 'food'},
            {'type': 'cafe'},
            {'type': 'bar'},
            {'keyword': 'fast food'},
            {'keyword': 'pizza'},
            {'keyword': 'coffee'},
        ]
    }

def get_comprehensive_search_strategies():
    """
    Get comprehensive search strategies for Google Places API to find all food establishments.
    
    Returns:
        list: List of search parameter dictionaries
    """
    return [
        # Primary food establishment types
        {'type': 'restaurant'},
        {'type': 'food'},
        {'type': 'cafe'},
        {'type': 'bakery'},
        {'type': 'bar'},
        {'type': 'meal_takeaway'},
        {'type': 'meal_delivery'},
        
        # Additional specific types
        {'type': 'night_club'},
        {'type': 'liquor_store'},
        
        # Keyword-based searches for comprehensive coverage
        {'keyword': 'restaurant'},
        {'keyword': 'cafe'},
        {'keyword': 'food'},
        {'keyword': 'dining'},
        {'keyword': 'eatery'},
        {'keyword': 'bakery'},
        {'keyword': 'bar'},
        {'keyword': 'pub'},
        {'keyword': 'bistro'},
        {'keyword': 'deli'},
        {'keyword': 'fast food'},
        {'keyword': 'takeaway'},
        {'keyword': 'coffee'},
        {'keyword': 'ice cream'},
        {'keyword': 'pizza'},
        {'keyword': 'burger'},
        {'keyword': 'sandwich'},
        {'keyword': 'sushi'},
        {'keyword': 'chinese'},
        {'keyword': 'indian'},
        {'keyword': 'italian'},
        {'keyword': 'mexican'},
        {'keyword': 'thai'},
        {'keyword': 'japanese'},
        {'keyword': 'korean'},
        {'keyword': 'mediterranean'},
        {'keyword': 'american'},
        {'keyword': 'seafood'},
        {'keyword': 'steakhouse'},
        {'keyword': 'bbq'},
        {'keyword': 'vietnamese'},
        {'keyword': 'lebanese'},
        {'keyword': 'french'},
        {'keyword': 'halal'},
        {'keyword': 'vegetarian'},
        {'keyword': 'vegan'},
    ]
