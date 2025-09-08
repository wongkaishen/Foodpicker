from django.conf import settings

def google_maps_api_key(request):
    """Add Google Maps API key to template context."""
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
