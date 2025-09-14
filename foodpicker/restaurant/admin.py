from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant, ContactMessage, ApprovedRestaurant, GooglePlacesRestaurant

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cuisine_type',
        'price_range',
        'display_rating',
        'city',
        'approved',
        'display_contact',
        'submitted_by',
    )
    
    list_filter = (
        'approved',
        'cuisine_type',
        'price_range',
        'delivery_available',
        'takeout_available',
        'city',
    )
    
    search_fields = (
        'name',
        'description',
        'street_address',
        'city',
        'state',
        'country',
        'submitted_by__username',
    )
    
    readonly_fields = (
        'created_at',
        'updated_at',
        'submitted_by',
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'description',
                'cuisine_type',
                'price_range',
                'average_rating',
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'email',
                'website',
            )
        }),
        ('Business Details', {
            'fields': (
                ('opentime', 'closetime'),
                ('delivery_available', 'takeout_available'),
            )
        }),
        ('Location', {
            'fields': (
                'street_address',
                ('city', 'state'),
                ('postal_code', 'country'),
                ('latitude', 'longitude'),
            )
        }),
        ('Meta Information', {
            'fields': (
                'approved',
                'submitted_by',
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',),
        }),
    )
    
    actions = ['approve_restaurants']
    
    def display_rating(self, obj):
        """Display rating with stars"""
        stars = '★' * int(round(obj.average_rating))
        # Convert the float to string with 1 decimal place before passing to format_html
        rating = '{:.1f}'.format(obj.average_rating)
        return format_html('<span style="color: #FFD700;">{}</span> ({})', stars, rating)
    display_rating.short_description = 'Rating'
    
    def display_contact(self, obj):
        """Display contact information"""
        contacts = []
        if obj.phone:
            contacts.append(f'📞 {obj.phone}')
        if obj.email:
            contacts.append(f'✉ {obj.email}')
        return ' | '.join(contacts) if contacts else '-'
    display_contact.short_description = 'Contact'
    
    def approve_restaurants(self, request, queryset):
        """Approve selected restaurants and move them to ApprovedRestaurant."""
        approved_count = 0
        for restaurant in queryset:
            if not restaurant.approved:
                restaurant.approve()
                approved_count += 1
        self.message_user(request, f'{approved_count} restaurant(s) were successfully approved and moved to Approved Restaurants.')
    approve_restaurants.short_description = 'Approve selected restaurants'
    
    
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"

admin.site.register(ContactMessage, ContactMessageAdmin)

# Register ApprovedRestaurant in the admin panel
@admin.register(ApprovedRestaurant)
class ApprovedRestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'cuisine_type',
        'price_range',
        'average_rating',
        'city',
        'submitted_by',
    )
    search_fields = (
        'name',
        'description',
        'street_address',
        'city',
        'state',
        'country',
        'submitted_by__username',
    )
    readonly_fields = (
        'created_at',
        'updated_at',
        'submitted_by',
    )

@admin.register(GooglePlacesRestaurant)
class GooglePlacesRestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'google_place_id_short',
        'cuisine_type',
        'establishment_type',
        'display_rating',
        'price_range',
        'business_status',
        'is_cache_valid_display',
        'last_updated_from_google',
    )
    
    list_filter = (
        'cuisine_type',
        'establishment_type',
        'price_range',
        'business_status',
        'delivery_available',
        'takeout_available',
        'is_open_24_hours',
        'last_updated_from_google',
    )
    
    search_fields = (
        'name',
        'google_place_id',
        'formatted_address',
        'phone',
    )
    
    readonly_fields = (
        'google_place_id',
        'last_updated_from_google',
        'created_at',
        'updated_at',
        'cache_expires_at',
        'display_photo_count',
        'display_reviews_count',
        'display_google_types',
    )
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'google_place_id',
                'formatted_address',
                'business_status',
            )
        }),
        ('Location', {
            'fields': (
                'latitude',
                'longitude',
            )
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'website',
                'google_url',
            )
        }),
        ('Restaurant Details', {
            'fields': (
                'cuisine_type',
                'establishment_type',
                'price_level',
                'price_range',
            )
        }),
        ('Ratings & Reviews', {
            'fields': (
                'rating',
                'user_ratings_total',
                'display_reviews_count',
            )
        }),
        ('Operating Hours', {
            'fields': (
                'opening_hours_text',
                'is_open_now',
                'is_open_24_hours',
            )
        }),
        ('Service Options', {
            'fields': (
                'delivery_available',
                'takeout_available',
            )
        }),
        ('Google Data', {
            'fields': (
                'display_google_types',
                'display_photo_count',
            )
        }),
        ('Cache Information', {
            'fields': (
                'last_updated_from_google',
                'cache_expires_at',
                'created_at',
                'updated_at',
            )
        }),
    )
    
    actions = ['refresh_from_google', 'mark_cache_expired']
    
    def google_place_id_short(self, obj):
        """Display shortened Place ID"""
        if obj.google_place_id:
            return f"{obj.google_place_id[:20]}..."
        return "-"
    google_place_id_short.short_description = "Place ID"
    
    def display_rating(self, obj):
        """Display rating with stars"""
        if obj.rating > 0:
            stars = "⭐" * int(obj.rating)
            return format_html(
                f'<span title="{obj.rating}/5.0">{stars} {obj.rating} ({obj.user_ratings_total} reviews)</span>'
            )
        return "-"
    display_rating.short_description = "Rating"
    
    def is_cache_valid_display(self, obj):
        """Display cache validity status"""
        is_valid = obj.is_cache_valid()
        color = "green" if is_valid else "red"
        status = "Valid" if is_valid else "Expired"
        return format_html(f'<span style="color: {color};">{status}</span>')
    is_cache_valid_display.short_description = "Cache Status"
    
    def display_photo_count(self, obj):
        """Display number of photos"""
        count = len(obj.photo_references) if obj.photo_references else 0
        return f"{count} photos"
    display_photo_count.short_description = "Photos"
    
    def display_reviews_count(self, obj):
        """Display number of cached reviews"""
        count = len(obj.reviews_data) if obj.reviews_data else 0
        return f"{count} cached reviews"
    display_reviews_count.short_description = "Cached Reviews"
    
    def display_google_types(self, obj):
        """Display Google place types"""
        if obj.google_types:
            types_str = ", ".join(obj.google_types[:5])  # Show first 5 types
            if len(obj.google_types) > 5:
                types_str += f" (+{len(obj.google_types) - 5} more)"
            return types_str
        return "-"
    display_google_types.short_description = "Google Types"
    
    def refresh_from_google(self, request, queryset):
        """Admin action to refresh selected restaurants from Google"""
        from .views import get_or_fetch_google_restaurant
        
        updated_count = 0
        for restaurant in queryset:
            try:
                updated_restaurant, message = get_or_fetch_google_restaurant(
                    restaurant.google_place_id, 
                    force_refresh=True
                )
                if updated_restaurant:
                    updated_count += 1
            except Exception as e:
                pass  # Skip errors
        
        self.message_user(
            request,
            f'Successfully refreshed {updated_count} restaurants from Google Places API.'
        )
    refresh_from_google.short_description = "Refresh selected from Google Places API"
    
    def mark_cache_expired(self, request, queryset):
        """Admin action to mark cache as expired"""
        from django.utils import timezone
        queryset.update(cache_expires_at=timezone.now())
        self.message_user(
            request,
            f'Marked cache as expired for {queryset.count()} restaurants.'
        )
    mark_cache_expired.short_description = "Mark cache as expired"

