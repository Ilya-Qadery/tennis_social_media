# Varzesha (ورزشا) - Tennis Community Platform

A Django-based tennis community and training platform for the Iranian market, following the HackSoft style guide.

## Features

### Phase 1 (MVP)

- **User Authentication**: Iranian phone number-based authentication with SMS verification
- **Player Profiles**: NTRP rating system, play style, statistics
- **Coach Profiles**: Verified coach listings with pricing and specialties
- **Court Discovery**: Find tennis courts by location, surface type, amenities
- **Match Scheduling**: Create, join, and manage tennis matches
- **Training Logs**: Log training sessions with drills and track progress
- **Training Goals**: Set and track personal training goals

## Architecture

This project follows the [HackSoft Django Styleguide](https://github.com/HackSoftware/Django-Styleguide):

```
varzesha/
├── config/                 # Django configuration
│   ├── django/            # Settings (base, local, production, test)
│   ├── env.py             # Environment configuration
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py            # WSGI application
├── varzesha/              # Main application
│   ├── core/              # Base models, exceptions, utilities
│   ├── users/             # User authentication & management
│   ├── profiles/          # Player & Coach profiles
│   ├── courts/            # Court discovery & reviews
│   ├── matches/           # Match scheduling & scoring
│   └── trainings/         # Training logs, drills & goals
└── requirements/          # Dependencies
    ├── base.txt
    ├── local.txt
    └── production.txt
```

### Key Patterns

- **Services**: Business logic in `services.py` with naming `<entity>_<action>`
- **Selectors**: Data fetching in `selectors.py` for read operations
- **APIs**: Thin HTTP layer in `apis/` directory
- **Models**: Validation in `clean()` methods, database constraints

## Quick Start

### 1. Clone and Setup

```bash
cd varzesha
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/local.txt
```

### 2. Environment Variables

```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Database Setup

```bash
# Create PostgreSQL database
createdb varzesha

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

### 5. Run Celery (for async tasks)

```bash
celery -A config worker -l info
```

## API Documentation

Once running, access the API documentation at:

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/users/auth/register/` | POST | Register with phone & password |
| `/api/users/auth/send-code/` | POST | Request SMS verification code |
| `/api/users/auth/verify/` | POST | Verify phone with code |
| `/api/users/auth/login/` | POST | Login with phone & password |
| `/api/users/me/` | GET/PATCH | Get/update current user |
| `/api/users/me/change-password/` | POST | Change password |

### Profiles

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/profiles/player/me/` | GET/POST/PATCH | Player profile management |
| `/api/profiles/players/` | GET | List players with filters |
| `/api/profiles/coach/me/` | GET/POST/PATCH | Coach profile management |
| `/api/profiles/coaches/` | GET | List coaches with filters |
| `/api/profiles/coaches/<id>/` | GET | Public coach profile |

### Courts

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/courts/` | GET | List courts with filters |
| `/api/courts/cities/` | GET | List cities with courts |
| `/api/courts/<id>/` | GET | Court details |
| `/api/courts/<id>/reviews/` | GET/POST | Court reviews |

### Matches

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/matches/` | GET | List user's matches |
| `/api/matches/create/` | POST | Create a match |
| `/api/matches/available/` | GET | List available public matches |
| `/api/matches/stats/` | GET | User match statistics |
| `/api/matches/<id>/` | GET/PATCH | Match details/update |
| `/api/matches/<id>/join/` | POST | Join a match |
| `/api/matches/<id>/leave/` | POST | Leave a match |
| `/api/matches/<id>/cancel/` | POST | Cancel a match |
| `/api/matches/<id>/score/` | POST | Record match score |

### Training

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trainings/drills/` | GET | List drills |
| `/api/trainings/drills/<id>/` | GET | Drill details |
| `/api/trainings/sessions/` | GET | List training sessions |
| `/api/trainings/sessions/create/` | POST | Create session |
| `/api/trainings/sessions/stats/` | GET | Training statistics |
| `/api/trainings/sessions/<id>/` | GET/PATCH/DELETE | Session management |
| `/api/trainings/sessions/<id>/drills/` | POST | Add drill to session |
| `/api/trainings/goals/` | GET | List goals |
| `/api/trainings/goals/create/` | POST | Create goal |
| `/api/trainings/goals/<id>/` | GET/PATCH | Goal management |
| `/api/trainings/goals/<id>/progress/` | POST | Update goal progress |

## Iranian-Specific Features

- **Phone Authentication**: Uses Iranian mobile format (09XXXXXXXXX)
- **SMS Verification**: Integrated with Kavenegar (Iranian SMS provider)
- **Currency**: Prices in Iranian Toman (IRT)
- **Cities**: Pre-configured for major Iranian cities
- **RTL Support**: Ready for Persian (Farsi) localization

## Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=varzesha
```

## Deployment

### Production Settings

```bash
export DJANGO_SETTINGS_MODULE=config.django.production
```

### Using Docker (recommended)

```bash
# Build and run
docker-compose up --build
```

## Contributing

1. Follow the HackSoft style guide
2. Write tests for services and selectors
3. Use type hints where appropriate
4. Keep APIs thin - business logic goes in services

## License

MIT License
