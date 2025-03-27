# FoodPicker

FoodPicker is a Django-based web application that helps users discover restaurants based on their location. Users can search for nearby restaurants, filter by distance, and submit new restaurant entries.

## Features

- **Map Display:** View all restaurants and user location on an interactive map.
- **Search & Filter:** Filter restaurants by radius (2km, 5km, 10km, 15km).
- **Restaurant Submission:** Users can add new restaurants by providing an address or pinpointing a location on the map.
- **Geolocation & Distance Calculation:** Uses the Haversine formula to determine the distance between the user and restaurants.
- **Approval System:** New restaurant submissions require admin approval before appearing on the map.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django
- PostgreSQL (or your preferred database)
- create env if you prefer

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/FoodPicker.git
   cd FoodPicker
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
   
3. Run migrations:
   ```sh
   python manage.py migrate
   ```

4. Start the development server:
   ```sh
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`

## Usage

1. **View Restaurants:** Navigate to the map view to see all available restaurants.
2. **Filter by Distance:** Use the radius filter to find restaurants within a certain range.
3. **Submit a Restaurant:** Click "Add Restaurant" and enter details or select a location on the map.
4. **Admin Approval:** Submitted restaurants will be reviewed by an admin before appearing on the map.

## Technologies Used
- Django (Python)
- PostgreSQL
- JavaScript (AJAX, Leaflet.js for maps)
- OpenStreetMap & Nominatim API


## License
This project is licensed under the MIT License.

## Contact
For questions or collaboration, reach out to Micheakl at wongkaishen2003@hotmail.com or foodpicker2024@gmail.com or open an issue on GitHub.
