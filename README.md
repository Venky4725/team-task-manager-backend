# Team Task Manager - Backend

A production-ready FastAPI backend for team task management with JWT authentication, PostgreSQL database, and role-based access control.

## Features

- **JWT Authentication** - Secure token-based authentication
- **Role-Based Access Control** - Admin and Member roles with different permissions
- **PostgreSQL Database** - Robust relational database with SQLAlchemy ORM
- **RESTful API** - Clean and well-documented API endpoints
- **Database Migrations** - Alembic for database version control
- **Input Validation** - Pydantic schemas for request/response validation
- **CORS Support** - Cross-origin resource sharing enabled
- **Error Handling** - Global exception handling with proper HTTP status codes

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **Pydantic** - Data validation
- **JWT** - JSON Web Tokens for authentication
- **Passlib** - Password hashing with bcrypt

## Database Schema

### Users
- id, name, email, password_hash, role, created_at

### Projects
- id, name, description, created_by, created_at

### Project Members
- id, project_id, user_id

### Tasks
- id, title, description, status, priority, deadline, project_id, assigned_to, created_by, created_at

## Installation

### Prerequisites
- Python 3.8+
- PostgreSQL database (Railway or local)

### Setup Steps

1. **Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Configure environment variables**

Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

Edit `.env`:
```
DATABASE_URL=postgresql://postgres:uLEhsWhIwJOQOdWqBtygZXdNHITFaWWh@postgres.railway.internal:5432/railway
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

6. **Initialize database**

The application will automatically create tables on first run. Alternatively, use Alembic:

```bash
alembic upgrade head
```

7. **Seed demo data**
```bash
python app/seed.py
```

This creates demo accounts:
- **Admin**: admin@example.com / password123
- **Member 1**: john@example.com / password123
- **Member 2**: jane@example.com / password123

## Running the Application

### Development Mode
```bash
python run.py
```

The API will be available at: `http://localhost:8000`

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user info

### Projects
- `POST /api/projects` - Create project
- `GET /api/projects` - Get all projects (with pagination & search)
- `GET /api/projects/{id}` - Get single project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project
- `POST /api/projects/{id}/members` - Add member to project

### Tasks
- `POST /api/tasks` - Create task
- `GET /api/tasks` - Get all tasks (with filters)
- `GET /api/tasks/{id}` - Get single task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/recent-tasks` - Get recent tasks

## Role-Based Permissions

### Admin
- Full access to all projects and tasks
- Can create, update, and delete any project
- Can create, update, and delete any task
- Can assign members to projects

### Member
- Access only to assigned projects
- Can view assigned tasks
- Can update status of own assigned tasks
- Cannot delete projects or tasks

## Database Migrations

### Create a new migration
```bash
alembic revision --autogenerate -m "description"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Railway Deployment

### Prerequisites
- Railway account
- Railway CLI installed

### Deployment Steps

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize project**
```bash
railway init
```

4. **Add PostgreSQL database**
```bash
railway add
```
Select PostgreSQL from the list.

5. **Set environment variables**

In Railway dashboard, add:
- `DATABASE_URL` (automatically set by Railway)
- `SECRET_KEY`
- `ALGORITHM=HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES=30`

6. **Deploy**
```bash
railway up
```

7. **Run seed script** (optional)
```bash
railway run python app/seed.py
```

### Railway Configuration

Create `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Project Structure

```
backend/
├── app/
│   ├── database/
│   │   ├── connection.py      # Database connection
│   │   └── base.py            # Base model
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── project_member.py
│   │   └── task.py
│   ├── schemas/               # Pydantic schemas
│   │   ├── user.py
│   │   ├── auth.py
│   │   ├── project.py
│   │   └── task.py
│   ├── routes/                # API routes
│   │   ├── auth.py
│   │   ├── projects.py
│   │   ├── tasks.py
│   │   └── dashboard.py
│   ├── middleware/            # Middleware
│   │   ├── auth.py
│   │   └── roles.py
│   ├── services/              # Business logic
│   │   ├── auth_service.py
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   └── dashboard_service.py
│   ├── utils/                 # Utilities
│   │   ├── security.py
│   │   ├── responses.py
│   │   └── helpers.py
│   ├── main.py                # FastAPI app
│   └── seed.py                # Database seeding
├── alembic/                   # Database migrations
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables
├── .env.example              # Environment template
├── alembic.ini               # Alembic configuration
├── run.py                    # Development server
└── README.md                 # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | Required |
| SECRET_KEY | JWT secret key | Required |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiration time | 30 |

## Security Features

- Password hashing with bcrypt
- JWT token authentication
- Role-based access control
- SQL injection prevention (SQLAlchemy ORM)
- Input validation (Pydantic)
- CORS configuration
- Secure password requirements

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error

## Testing

### Manual Testing
Use the Swagger UI at `/docs` to test endpoints interactively.

### API Testing Tools
- Postman
- Insomnia
- cURL

Example cURL request:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"password123"}'
```

## Troubleshooting

### Database Connection Issues
- Verify DATABASE_URL is correct
- Ensure PostgreSQL is running
- Check network connectivity

### Import Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Migration Issues
- Delete alembic/versions/* and recreate: `alembic revision --autogenerate -m "initial"`
- Or use automatic table creation (already configured)

## Support

For issues or questions, please check:
- API documentation at `/docs`
- Error logs in console
- Database connection settings

## License

MIT License
