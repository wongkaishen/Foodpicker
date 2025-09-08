# Google Maps API Migration Setup Guide

## Overview
Your FoodPicker application has been migrated from Leaflet/OpenStreetMap to Google Maps API. This guide explains what you need to do to complete the setup.

## 1. Get Google Maps API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the following APIs:
   - **Maps JavaScript API** (for displaying maps)
   - **Geocoding API** (for address search and geocoding)
   - **Places API** (optional, for enhanced place search)

4. Create an API key:
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" > "API Key"
   - Copy the generated API key

## 2. Add API Key to Environment Variables

Add your Google Maps API key to your environment variables:

### For local development (.env file):
```
GOOGLE_MAPS_API_KEY=your_api_key_here
```

### For production (environment variables):
Set the environment variable `GOOGLE_MAPS_API_KEY` with your API key value.

## 3. Update Template Files

Replace `YOUR_GOOGLE_MAPS_API_KEY` in the following files with your actual API key:

1. `foodpicker/restaurant/templates/homepage/content/map.html` (line ~366)
2. `foodpicker/restaurant/templates/homepage/content/form.html` (line ~354)
3. `foodpicker/restaurant/templates/homepage/content/restaurant_detail.html` (line ~143)

Or better yet, update the templates to use the environment variable:

Replace:
```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_GOOGLE_MAPS_API_KEY&libraries=places&callback=initMap"></script>
```

With:
```html
<script async defer src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_API_KEY }}&libraries=places&callback=initMap"></script>
```

And add this to your `settings.py`:
```python
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY')

# Add to context processors
TEMPLATES = [
    {
        # ... other settings ...
        'OPTIONS': {
            'context_processors': [
                # ... other processors ...
                'django.template.context_processors.request',
            ],
        },
    },
]
```

## 4. Update Requirements

Install the updated requirements:
```bash
pip install -r requirements.txt
```

## 5. API Usage and Quotas

**Important**: Google Maps API is not free like OpenStreetMap. You get:
- $200 free credit per month
- After that, you pay per API call

Monitor your usage in the Google Cloud Console to avoid unexpected charges.

## 6. Security Considerations

1. **Restrict your API key**: In Google Cloud Console, restrict your API key to:
   - Specific APIs (only the ones you enabled)
   - HTTP referrers (your domain only)

2. **Never commit API keys**: Make sure your API key is in environment variables, not hardcoded.

## Files Modified

The following files have been updated to use Google Maps:

### Frontend Templates:
- `restaurant/templates/homepage/content/map.html` - Main map page
- `restaurant/templates/homepage/content/form.html` - Restaurant submission form
- `restaurant/templates/homepage/content/restaurant_detail.html` - Individual restaurant page

### Backend:
- `restaurant/views.py` - Updated geocoding function
- `restaurant/static/js/accounts/map.js` - Static JavaScript file

### Configuration:
- `requirements.txt` - Removed django-leaflet, added requests
- `README.md` - Updated technology stack

## Testing

After setting up your API key:

1. Test the main map view (`/map/`)
2. Test restaurant submission form
3. Test individual restaurant detail pages
4. Verify geocoding works when adding new restaurants

## Troubleshooting

1. **Maps not loading**: Check browser console for API key errors
2. **Geocoding not working**: Verify Geocoding API is enabled
3. **Quota exceeded**: Check your Google Cloud Console for usage limits

## Benefits of Google Maps

1. **Better accuracy**: More precise geocoding and mapping
2. **Rich features**: Street view, satellite imagery, traffic data
3. **Professional appearance**: High-quality map styling
4. **Reliable service**: Enterprise-grade infrastructure

## Cost Considerations

- Monitor usage to stay within free tier
- Consider implementing caching for geocoding results
- Set up billing alerts in Google Cloud Console

For any issues, refer to the [Google Maps Platform documentation](https://developers.google.com/maps/documentation).
