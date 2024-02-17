# Vision Board Project

This project is a web application that allows users to create and manage vision boards, sub-boards, goals, tasks, and collaborate with others on their goals and tasks.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YeganeGholipour/Vision-Board.git
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the development server:
```bash
python manage.py runserver
```

3. Access the application at [http://localhost:8000](http://localhost:8000)

## File Structure
```
vision-board-project/
│
├── board/
│   ├── models.py
│   ├── views.py
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── manage.py
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── celeryconfig.py
```

## Configuration

- Edit `config/settings.py` to configure the project settings.
- Configure Celery tasks in `celeryconfig.py`.

## Celery

This project uses Celery for asynchronous task processing. To run Celery worker:

```bash
celery -A config worker -l info
```

## RabbitMQ

This project uses RabbitMQ as the message broker for Celery. Make sure RabbitMQ is installed and running. Update the Celery configuration in `celeryconfig.py` to point to the RabbitMQ server.

## Docker

This project includes Docker support. To build and run the Docker container:


## Swagger Documentation

This project includes Swagger documentation to help you understand and interact with the API endpoints. You can access the Swagger UI by following these steps:

1. Start the Django development server:

   ```bash
   python manage.py runserver
   ```
2. Open your web browser and navigate to the Swagger UI endpoint:

   ```bash
   http://localhost:8000/docs/
   ```
   
Explore the API endpoints:

Use the Swagger UI interface to view and interact with the available API endpoints.
Each endpoint includes detailed information on parameters, request bodies, and responses.

## Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Credits

- Django REST Framework
- Font Awesome
- Celery
- Docker
