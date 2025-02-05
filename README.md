# Book Store App

A Django-based Bookstore application with a PostgreSQL database, containerized using Docker.

## Features
- User authentication (login, register)
- Browse books by category
- Add books to cart and checkout
- Leave reviews for books
- Admin panel for managing books and users
- API endpoints with Django Rest Framework (optional)

## Project Structure
```
book_store/
├── books/                  # Books app (models, views, serializers, templates)
│   ├── management/         # Custom Django management commands
│   ├── migrations/         # Database migrations
│   ├── static/             # CSS and images for frontend
│   ├── templates/          # HTML templates
│   ├── views.py            # Django views
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   ├── serializers.py      # API serializers (if applicable)
│   └── tests.py            # Unit tests
│
├── book_store/             # Main project settings
│   ├── settings.py         # Django settings
│   ├── urls.py             # Global URL configurations
│   ├── wsgi.py             # WSGI entry point
│
├── scripts/                # Custom scripts (e.g., creating an admin user)
│   ├── create_admin.py     # Script to create a superuser
│
├── static/                 # Static files collected for deployment
├── templates/              # Global HTML templates
├── manage.py               # Django management tool
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker container instructions
├── docker-compose.yml      # Docker Compose setup
├── bookstore_backup.sql    # PostgreSQL backup file
└── .env                    # Environment variables (not included in repo)
```

## Prerequisites
- [Docker](https://www.docker.com/get-started) installed
- [Docker Compose](https://docs.docker.com/compose/install/) installed

## Running the Project in Docker

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/book_store.git
   cd book_store
   ```

2. **Create an `.env` file** in the root directory and add the following:
   ```env
   ADMIN_USERNAME=admin
   ADMIN_EMAIL=admin@example.com
   ADMIN_PASSWORD=admin123
   DATABASE_URL=postgres://bookstore_user:secure_password@db:5432/bookstore_db
   ```

3. **Build and start the containers**
   ```sh
   docker-compose up --build -d
   ```

4. **Check running containers**
   ```sh
   docker ps
   ```

5. **Apply database migrations**
   ```sh
   docker exec -it bookstore_app python manage.py migrate
   ```

6. **Create a superuser (if not created automatically)**
   ```sh
   docker exec -it bookstore_app python manage.py createsuperuser
   ```

7. **Access the application**
   - Open [http://localhost:8000](http://localhost:8000) in your browser
   - Admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)

## Stopping & Cleaning Up

To stop the containers:
```sh
docker-compose down
```

To remove all Docker containers, networks, and volumes:
```sh
docker system prune -a --volumes
```

## Troubleshooting

- **Container not starting?**
  ```sh
  docker logs bookstore_app
  docker logs bookstore_db
  ```
  
- **Database errors?**
  ```sh
  docker exec -it bookstore_db psql -U bookstore_user -d bookstore_db
  ```
  Run SQL commands to check the tables.

## Contributing
Pull requests are welcome! Please open an issue first for discussion.

## License
MIT License

