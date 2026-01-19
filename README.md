# NaijaCal - AI-Powered Nigerian Food Calorie Tracker

> Track your calories with AI - Built for Nigerian cuisine

![Django](https://img.shields.io/badge/Django-5.0-green)
![React](https://img.shields.io/badge/React-19.1-blue)
![Python](https://img.shields.io/badge/Python-3.12-yellow)
![AI](https://img.shields.io/badge/AI-OpenAI-purple)
![Status](https://img.shields.io/badge/Status-Live-success)

## 🎯 What It Does

NaijaCal helps Nigerians track their daily calorie intake with a focus on local foods. Just paste what you ate in natural language - the AI handles the rest.

**Live Demo:** https://health-app-frontend1.onrender.com *(⚠️ First load takes ~30s - free tier limitation)*

**Example:**
```
Breakfast: 2 slices of bread with eggs
Lunch: Jollof rice and chicken
Dinner: Eba and Egusi soup
Snacks: Puff puff and zobo
```
→ AI parses it → Returns total calories

## ✨ Key Features

- 🍲 **100+ Nigerian Foods** - Jollof rice, Eba, Egusi, Moi moi, Suya, and more
- 🤖 **AI-Powered Parsing** - OpenAI understands natural language food logs
- 🔐 **Secure Authentication** - User accounts to protect API access
- 📊 **Instant Calculations** - Real-time calorie tracking
- 🎨 **Clean Interface** - Modern React UI with Tailwind CSS
- 🛡️ **Rate Limited** - 10 requests/hour to prevent API abuse

## 🛠️ Tech Stack

### Backend
- **Django 5.0** - Python web framework
- **Django REST Framework** - RESTful API
- **OpenAI GPT-4o-mini** - Natural language processing
- **PostgreSQL (Supabase)** - Primary database
- **SimpleJWT** - Authentication
- **UptimeRobot** - Keep-alive monitoring

### Frontend  
- **React 19** - UI framework
- **Tailwind CSS** - Styling
- **localStorage** - Token persistence

### Infrastructure
- **Docker & Docker Compose** - Local development
- **Render** - Web hosting (Backend + Frontend)
- **Supabase** - Managed PostgreSQL Database
- **UptimeRobot** - Prevents free tier hibernation

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Node.js 18+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- PostgreSQL (or use SQLite for local dev)

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/sethnwoks/Health_App.git
cd Health_App/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your OPENAI_API_KEY and other settings

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Backend runs at `http://localhost:8000`

### Frontend Setup

```bash
cd ../frontend/frontend

# Install dependencies
npm install

# Set up environment
cp .env.example .env
# Add REACT_APP_API_URL=http://localhost:8000

# Start development server
npm start
```

Frontend runs at `http://localhost:3000`

### Docker Setup (Alternative)

```bash
# From project root
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

## 📝 Environment Variables

### Backend (`.env`)
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your-django-secret-key

# Database (Supabase)
# IMPORTANT: Use the Session Pooler URL (Port 6543) for IPv4 compatibility on Render
DATABASE_URL=postgresql://postgres.[REF]:[PASS]@aws-0-[REGION].pooler.supabase.com:6543/postgres

# Optional
DEBUG=False
ALLOWED_HOSTS=.onrender.com,localhost
CORS_ALLOWED_ORIGINS=https://health-app-frontend1.onrender.com
```

### Frontend (`.env`)
```bash
REACT_APP_API_URL=http://localhost:8000

# For production
# REACT_APP_API_URL=https://your-backend.onrender.com
```

## 🎮 How to Use

### 1. Register an Account
```bash
POST /register
{
  "username": "yourname",
  "password": "yourpass",
  "email": "you@email.com"
}
# Returns: access token + refresh token
```

### 2. Login (if already registered)
```bash
POST /api/token/
{
  "username": "yourname",
  "password": "yourpass"
}
# Returns: access token + refresh token
```

### 3. Parse Food Log
```bash
POST /parse-log
Headers: {
  "Authorization": "Bearer <your_access_token>"
}
Body: {
  "foodLog": "Breakfast: Jollof rice with chicken. Snacks: Puff puff"
}
```

**Response:**
```json
{
  "status": "success",
  "parsed_items": [
    {
      "item": "jollof rice",
      "quantity": "1 plate",
      "total_calories": 650
    },
    {
      "item": "chicken",
      "quantity": "1 piece",
      "total_calories": 239
    },
    {
      "item": "puff puff",
      "quantity": "3 pieces",
      "total_calories": 400
    }
  ],
  "total_calories": 1289
}
```

### 4. Get Your Profile
```bash
GET /me
Headers: {
  "Authorization": "Bearer <your_access_token>"
}
```

## 🔌 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/register` | POST | No | Create new account |
| `/api/token/` | POST | No | Login / Get tokens |
| `/api/token/refresh/` | POST | No | Refresh access token |
| `/parse-log` | POST | Yes | Parse food log & calculate calories |
| `/me` | GET | Yes | Get current user info |

## 🍽️ Supported Foods (100+)

**Swallows & Staples:** Eba, Fufu, Amala, Pounded yam, Semovita, White rice, Brown rice, Jollof rice, Fried rice

**Soups:** Egusi, Ogbono, Afang, Efo riro, Okro, Banga, Nsala, Oha, Ewedu, Gbegiri

**Proteins:** Beef, Chicken, Fish, Goat meat, Turkey, Suya

**Snacks:** Puff puff, Akara, Moi moi, Meat pie, Shawarma, Kuli kuli

**Staples:** Bread, Pasta, Noodles, Indomie, Beans, Yam, Plantain

**Drinks:** Zobo, Chapman, Malt, Coke, Fanta, Sprite

[See full list in `backend/api/utils.py`]

## 📁 Project Structure

```
Health_App/
├── backend/
│   ├── api/                    # Main Django app
│   │   ├── models.py          # Database models
│   │   ├── views.py           # API endpoints (auth + parsing)
│   │   ├── utils.py           # Food database & AI logic
│   │   └── urls.py            # URL routing
│   ├── core/                  # Django settings
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Backend container
│   └── manage.py
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── App.js        # Main React component
│       │   └── App.css       # Styles
│       ├── package.json      # Node dependencies
│       └── Dockerfile        # Frontend container
├── docker-compose.yml        # Multi-container setup
└── README.md
```

## 🔒 Security Features

- **JWT Authentication** - Stateless token-based auth
- **Rate Limiting** - 10 requests/hour per user (prevents API abuse)
- **Password Hashing** - Django's built-in PBKDF2
- **CORS Protection** - Configured allowed origins
- **Environment Variables** - Sensitive keys not in code

## ⚡ Performance

- **Cold Start:** ~30s on Render free tier (first request after inactivity)
- **Subsequent Requests:** <2s
- **Rate Limit:** 10 parses/hour per user (to control OpenAI costs)

## 🚧 Known Limitations & Future Plans

**Current Limitations:**
- Limited to 100+ foods (expanding)
- No portion size tracking (uses AI estimates)
- Cold starts on free hosting tier
- No historical tracking (single session only)

**Planned Features:**
- [ ] User dashboard with daily/weekly history
- [ ] Nutritional breakdown (protein, carbs, fats)
- [ ] Food database admin panel
- [ ] Barcode scanning
- [ ] Meal planning suggestions
- [ ] Export data to CSV
- [ ] Mobile app (React Native)
- [ ] Recipe calorie calculator

## 💡 How It Works

1. **User Input:** Paste food log in natural language
2. **AI Parsing:** OpenAI GPT-4 extracts food items, quantities, and units
3. **Database Lookup:** Match foods against Nigerian food database
4. **Calculation:** Compute calories based on quantity × calories_per_100g
5. **Response:** Return structured JSON with total calories

**Example Flow:**
```
"I ate 2 plates of jollof rice"
    ↓
OpenAI extracts: {food: "jollof rice", quantity: 2, unit: "plate"}
    ↓
Database lookup: jollof rice = 130 cal/100g
    ↓
Calculate: 2 plates × 250g/plate × 130cal/100g = 650 calories
    ↓
Return: {"item": "jollof rice", "total_calories": 650}
```

## 🎓 What I Learned

This project demonstrates:
- **Full-Stack Development** - Django backend + React frontend
- **AI Integration** - OpenAI API for NLP tasks
- **Authentication** - JWT implementation with Django REST Framework
- **API Design** - RESTful endpoints with proper auth flow
- **Database Management** - PostgreSQL with Django ORM
- **Deployment** - Docker containerization + cloud hosting
- **Rate Limiting** - Protecting paid APIs from abuse
- **State Management** - React hooks + localStorage

## 🤝 Contributing

This is a portfolio/learning project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/CoolFeature`)
3. Commit changes (`git commit -m 'Add CoolFeature'`)
4. Push to branch (`git push origin feature/CoolFeature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file

## 👨‍💻 Author

**Seth Nwokolo**
- GitHub: [@sethnwoks](https://github.com/sethnwoks)

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- Nigerian nutrition data compiled from various sources
- Django & React communities for excellent documentation
- Built during apprenticeship to demonstrate full-stack + AI skills

---

⭐️ **Star this repo if you found it useful!**

💬 **Questions?** Open an issue or reach out on LinkedIn

🚀 **Hire me?** I'm actively looking for backend/full-stack developer roles in Lagos or remote!
