# CallerID-Pro - User Identification and Spam Detection API

CallerID-Pro is a REST API built using Django for user identification, spam detection, and phone number lookup. It provides functionalities for user registration, authentication, contact searching, and marking numbers as spam.

## Features

- **User Registration & Authentication**: Secure user signup, login, and JWT-based authentication.
- **Phone Number Search**: Look up users based on phone numbers.
- **Name Search**: Search users by name and retrieve associated details.
- **Spam Reporting**: Users can report spam numbers to warn others.
- **Access Control**: User email is only visible if the requester is in their contact list.

## Tech Stack

- **Backend**: Django, Django REST Framework (DRF)
- **Database**: MySQL
- **Authentication**: JWT-based authentication
- **Deployment**: Gunicorn, Nginx, Docker (optional)

## Installation

### Prerequisites
- Python 3.13+
- MySQL Server (Running in the background)
- Virtual Environment (recommended)

### Setup
1. **Clone the Repository**
   ```sh
   git clone https://github.com/niteshmauryac7r/CallerID-Pro.git
   cd instahyre
   ```
2. **Create a Virtual Environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set Up the Database**
   - Update the `.env` file with MySQL credentials.
   ```sh
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
5. **Populate Sample Data**
   ```sh
   python3 manage.py populate_data
   ```
6. **Run the Development Server**
   ```sh
   python3 manage.py runserver
   ```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|-------------|-------------|
| POST | `/api/users/` | Register a new user |
| POST | `/api/token/` | Login and obtain JWT |

### User Management
| Method | Endpoint | Description |
|--------|-------------|-------------|
| GET | `/api/users/search_by_name/?name={name}` | Search users by name |
| GET | `/api/users/search_by_phone/?phone_number={number}` | Search users by phone number |

### Spam Management
| Method | Endpoint | Description |
|--------|-------------|-------------|
| POST | `/api/spam/` | Mark a phone number as spam |

## Running Tests
```sh
python3 manage.py test
```

## Postman Collection
- To test the APIs, import `Instahyre.postman_collection.json` in Postman.
- Update the environment URL according to your system.
- Authorization Token is created in the login API under the key "access".
- Use "Authorization: Bearer <access token>" in request headers.

## Deployment
For production deployment, use:
```sh
gunicorn instahyre.wsgi:application --bind 0.0.0.0:8000
```
For Docker deployment, build and run the container:
```sh
docker-compose up --build
```

## Contact
For any queries, feel free to contact:
- **Email**: niteshmauryac7r.nm@gmail.com

## License
This project is licensed under the MIT License.

