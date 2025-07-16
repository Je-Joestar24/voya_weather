# VoyaWeather 🌦️

**VoyaWeather** is a modern, modular Django web application that helps users plan their travels and daily activities by providing up-to-date weather information for cities around the world. The app features user authentication, city search, saved and favorite places, and a beautiful, accessible UI.

---

## 🚀 Features

- **User Authentication**
  - Secure signup, login, and logout flows
  - Password validation and error feedback

- **Weather Dashboard**
  - View weather summaries for popular cities
  - Animated, responsive dashboard with highlights and call-to-action

- **City Search**
  - Search for any city and view current weather conditions
  - Results include temperature, weather description, and emoji icon

- **Saved Places**
  - Save cities to your personal list for quick access
  - Remove places from your saved list
  - See when you saved each place

- **Favorites**
  - Mark any saved city as a favorite for easy reference

- **Recently Viewed**
  - Automatically logs cities you view in detail
  - No duplicates: the most recently viewed city always appears at the top

- **Accessibility & Responsiveness**
  - Semantic HTML, ARIA labels, and alt text throughout
  - Fully responsive design using CSS Grid and Flexbox
  - Smooth CSS animations for enhanced user experience

- **Modular & Reusable Components**
  - Django class-based views and modular templates
  - Reusable cards, navbars, and search bars

- **Class-Based Views (CBVs)**
  - All major views use Django class-based views for modular, maintainable, and reusable logic
  - Easier to extend and customize for future features

---

## 🛠️ Prerequisites

- Python 3.10+
- PostgreSQL (running on port 5432)
- pip (or pipenv/poetry)

---

## 🗄️ Database Setup (PostgreSQL)

Before running the app, you must create the database and user in PostgreSQL:

```bash
# Open the PostgreSQL shell (psql) as a superuser, e.g.:
psql -U postgres

# Then run the following commands:
CREATE DATABASE voyaweather;
CREATE USER voyaweather WITH PASSWORD 'Voya@09';
GRANT ALL PRIVILEGES ON DATABASE voyaweather TO voyaweather;
```

- If you use a different database name, user, or password, update the values in `voya_weather/settings.py` accordingly.

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Je-Joestar24/voya_weather
   cd voya_weather
   ```

2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv env
   # On Windows:
   env\Scripts\activate
   # On macOS/Linux:
   source env/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the app:**
   - Open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🗂️ Project Structure

- `core/` – Main Django app (models, views, templates, **class-based views for all major features**)
- `static/` – CSS, JS, images
- `templates/` – HTML templates (modular, reusable)
- `manage.py` – Django management script

---

## 🌐 API & Integrations

- **Weather Data:** [OpenWeatherMap API](https://openweathermap.org/api)

---

## 🙏 Acknowledgements

- Django Project
- OpenWeatherMap
- All contributors

---

## 📣 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---