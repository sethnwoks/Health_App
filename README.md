# NaijaCal - Nigerian Food Calorie Tracker

> AI-powered calorie tracking app specialized for Nigerian cuisine

![Django](https://img.shields.io/badge/Django-5.0-green)
![React](https://img.shields.io/badge/React-19.1-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![Status](https://img.shields.io/badge/Status-Active-success)

## 🎯 Overview

NaijaCal is a full-stack web application that helps Nigerians track their calorie intake with support for local foods like Jollof Rice, Egusi Soup, Eba, and more. The app uses Google's Gemini AI to parse natural language food logs and calculate nutritional information.

**Live Demo:** [Add your Render URL here]

## ✨ Features

- 🍲 **Nigerian Food Database** - Comprehensive calorie data for local dishes (100+ foods)
- 🤖 **AI-Powered Parsing** - Uses Google Gemini to understand natural language food entries
- 📊 **Calorie Tracking** - Automatic calculation of total daily calories
- 🎨 **Modern UI** - Clean, responsive interface built with React and Tailwind CSS
- 🔐 **REST API** - Django REST Framework backend with CORS support

## 🛠️ Tech Stack

### Backend
- **Django 5.0** - Web framework
- **Django REST Framework** - API development
- **PostgreSQL** - Production database
- **Google Gemini AI** - Natural language processing
- **Gunicorn + Whitenoise** - Production server

### Frontend
- **React 19** - UI framework
- **Tailwind CSS** - Styling
- **Fetch API** - HTTP requests

### Deployment
- **Render** - Hosting platform
- **Docker** - Containerization (optional)

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL (for production)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/Health_App.git
cd Health_App/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your GEMINI_API_KEY in .env

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd ../frontend/frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Add REACT_APP_API_URL=http://localhost:8000

# Start development server
npm start
```

Visit `http://localhost:3000` to see the app.

## 📝 Environment Variables

### Backend (.env)
```
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=your_database_url  # For production
DEBUG=True  # Set to False in production
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:8000
```

## 🎮 Usage

1. **Paste your food log** - Enter what you ate in natural language:
   ```
   Breakfast: 2 slices of bread with eggs
   Lunch: Jollof rice with chicken
   Dinner: Eba and Egusi soup
   ```

2. **Click "Parse Log"** - AI processes your input

3. **View Results** - See parsed items and total calories

## 📁 Project Structure

```
Health_App/
├── backend/
│   ├── api/              # Main Django app
│   │   ├── models.py     # Database models
│   │   ├── views.py      # API endpoints
│   │   └── utils.py      # Food database & AI logic
│   ├── core/             # Django settings
│   └── requirements.txt
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── App.js    # Main React component
│       │   └── App.css   # Styles
│       └── package.json
└── docker-compose.yml    # Docker configuration
```

## 🔌 API Endpoints

### POST /parse-log
Parse natural language food log and calculate calories.

**Request:**
```json
{
  "foodLog": "Breakfast: Jollof rice and chicken"
}
```

**Response:**
```json
{
  "status": "success",
  "parsed_items": [
    {"food": "jollof rice", "quantity": "1 plate", "calories": 650},
    {"food": "chicken", "quantity": "1 piece", "calories": 250}
  ],
  "total_calories": 900
}
```

## 🎨 Screenshots

[Add screenshots here when deploying]

## 🚧 Current Development

- [x] Basic calorie tracking
- [x] AI-powered parsing
- [x] Nigerian food database
- [ ] User authentication
- [ ] Daily tracking history
- [ ] Nutritional breakdown (protein, carbs, fats)
- [ ] Mobile app version

## 🤝 Contributing

This is a personal learning project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Google Gemini AI for natural language processing
- Nigerian food calorie data compiled from various nutrition sources
- Built during apprenticeship at [Company Name]

---

⭐️ If you found this project helpful, please give it a star!
