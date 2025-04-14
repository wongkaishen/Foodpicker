# FoodPicker

FoodPicker is a Django-based web application that helps users discover restaurants based on their location. Users can search for nearby restaurants, filter by distance, and submit new restaurant entries. The application also includes an admin approval system for new submissions, ensuring data quality and accuracy.

## Features

- **Interactive Map Display:** View all restaurants and user location on an interactive map powered by Leaflet.js and OpenStreetMap.
- **Search & Filter:** Filter restaurants by radius (2km, 5km, 10km, 15km) to find the best options nearby.
- **Restaurant Submission:** Users can add new restaurants by providing an address or pinpointing a location on the map.
- **Geolocation & Distance Calculation:** Uses the Haversine formula to determine the distance between the user and restaurants.
- **Approval System:** New restaurant submissions require admin approval before appearing on the map.
- **Custom Filters:** Includes custom Django template filters for enhanced functionality.
- **Responsive Design:** Optimized for both desktop and mobile devices.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django
- PostgreSQL (or your preferred database)
- Virtual environment tools (e.g., `venv` or `virtualenv`)

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/FoodPicker.git
   cd FoodPicker
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Update the `DATABASES` setting in `foodpicker/base/settings.py` with your database credentials.

5. Run migrations:
   ```sh
   python manage.py migrate
   ```

6. Start the development server:
   ```sh
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000/`

## Usage

1. **View Restaurants:** Navigate to the map view to see all available restaurants.
2. **Filter by Distance:** Use the radius filter to find restaurants within a certain range.
3. **Submit a Restaurant:** Click "Add Restaurant" and enter details or select a location on the map.
4. **Admin Approval:** Submitted restaurants will be reviewed by an admin before appearing on the map.

## Project Structure

- `foodpicker/`: Core Django project files, including settings, URLs, and WSGI configuration.
- `restaurant/`: Contains the main app logic, including models, views, forms, and templates.
- `database/`: Includes SQL files for database setup and backups.
- `static/`: Static assets such as CSS, JavaScript, and images.
- `templates/`: HTML templates for the application.
- `env/`: Virtual environment directory (not included in the repository).

## Technologies Used

- **Backend:** Django (Python)
- **Frontend:** JavaScript, Leaflet.js, HTML, CSS
- **Database:** PostgreSQL
- **APIs:** OpenStreetMap & Nominatim API

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push to your fork.
4. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Security

For security-related issues, please refer to the `SECURITY.md` file or contact Micheakl at wongkaishen2003@hotmail.com or foodpicker2024@gmail.com.

## Contact

For questions or collaboration, reach out to Micheakl at wongkaishen2003@hotmail.com or foodpicker2024@gmail.com, or open an issue on GitHub.
