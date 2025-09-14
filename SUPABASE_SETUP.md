# Supabase Setup for Foodpicker

This guide will help you configure your Django Foodpicker app to store Google Places restaurant data in Supabase PostgreSQL database.

## 🚀 Setup Instructions

### 1. Get Your Supabase Credentials

1. Go to [Supabase](https://supabase.com) and sign in
2. Create a new project or use an existing one
3. Go to **Settings** → **Database**
4. In the **Connection String** section, you'll find:
   - Host: `db.xxxxxxxxxxxxx.supabase.co`
   - Database name: `postgres`
   - Username: `postgres.xxxxxxxxxxxxx`
   - Password: Your database password
   - Port: `5432`

### 2. Configure Environment Variables

Edit the `.env` file in your project root (`foodpicker/.env`) with your Supabase details:

```env
# Supabase Database Configuration
DB_NAME=postgres
DB_USER=postgres.your_supabase_reference
DB_PASSWORD=your_supabase_password_here
DB_HOST=db.your_project_ref.supabase.co
DB_PORT=5432

# Google Maps API Key (you already have this)
GOOGLE_MAPS_API_KEY=your_google_maps_api_key

# Django Secret Key (generate a new one for production)
SECRET_KEY=your_django_secret_key_here
```

### 3. Run Database Migrations

Once you've configured your `.env` file:

```bash
cd foodpicker
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

## 📊 What's New

### New Model: `GooglePlacesRestaurant`

A comprehensive model to store Google Places data including:
- 📍 Location data (lat/lng, formatted address)
- 📞 Contact information (phone, website, Google URL)
- 🍽️ Restaurant details (cuisine, establishment type, price range)
- ⭐ Ratings and reviews
- 🕒 Opening hours
- 📸 Photo references
- 🚚 Service options (delivery, takeout)
- 💾 Cache management (auto-expiry after 24 hours)

### Enhanced Functions

- **`save_google_place_to_supabase()`**: Saves Google Places data to Supabase
- **`get_or_fetch_google_restaurant()`**: Smart caching - gets from Supabase cache or fetches fresh from Google
- **Updated `get_google_restaurant_detail()`**: Now uses Supabase cache for faster loading

## 🔧 How It Works

1. **First Request**: When you visit a restaurant detail page, the app:
   - Checks Supabase for cached data
   - If not found or expired, fetches from Google Places API
   - Saves the fresh data to Supabase with 24-hour cache expiry

2. **Subsequent Requests**: The app serves data from Supabase cache for faster loading

3. **Cache Management**: Data automatically refreshes from Google after 24 hours

## 🎛️ Admin Panel Features

Visit `/admin/` to manage your restaurants:
- View all cached Google Places restaurants
- See cache status (valid/expired)
- Manually refresh data from Google Places API
- Filter by cuisine, establishment type, rating, etc.
- Bulk actions for cache management

## 📱 Testing the Integration

1. Start your Django server: `python manage.py runserver`
2. Visit: `http://127.0.0.1:8000/google-test/`
3. Click on any sample restaurant
4. Check the admin panel to see the data stored in Supabase

## 🔄 URLs Summary

- `/google-test/` - Test page with sample restaurants
- `/google-restaurant/<place_id>/` - Restaurant details (now cached in Supabase)
- `/admin/` - Django admin panel to manage cached data

## 🎯 Benefits

- **⚡ Faster Loading**: Cached data loads much faster than API calls
- **💰 Cost Savings**: Reduced Google Places API usage
- **📊 Data Analytics**: Store and analyze restaurant data
- **🔄 Smart Caching**: Automatic refresh when data is stale
- **📈 Scalability**: Handle more users with less API load

## 🛠️ Troubleshooting

### Database Connection Issues
- Double-check your Supabase credentials in `.env`
- Ensure your Supabase project is active
- Verify the connection string format

### Migration Issues
- Make sure all environment variables are set
- Run `python manage.py check` to verify configuration
- If needed, reset migrations: `python manage.py migrate --fake-initial`

### API Issues
- Verify your Google Maps API key is still valid
- Check API quotas in Google Cloud Console
- Review Django logs for detailed error messages

Your restaurant data is now stored in Supabase! 🎉
