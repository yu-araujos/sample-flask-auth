# Authentication Project for an API using Flask

This repository contains an authentication application for an API developed with Flask. The project includes user profile management features and access control to the API endpoints, using Flask, MySQL (via Docker), and Flask-Login for session management.

## Features
- User registration (via `/user` POST)
- Login and logout (via `/login` POST and `/logout` GET)
- Retrieve profile information (via `/user/<user_id>` GET)
- Change password (via `/user/<user_id>` PUT)
- User deletion (via `/user/<user_id>` DELETE)
- Access control based on roles and permissions (only allows updates and deletions for the current user or admins)

## Technologies Used
- **Python**: Main programming language
- **Flask**: Framework for building the API
- **MySQL**: Relational database for storing user data, managed via Docker
- **Flask-JWT-Extended**: For implementing authentication based on JSON Web Tokens (JWT)
- **Flask-Login**: For managing user sessions
- **Bcrypt**: For securely hashing and verifying passwords
- **Docker**: Used for setting up the MySQL environment using Docker Compose

## Endpoints

### `/login` (POST)
- Authenticates the user with username and password.
- Returns a success message if credentials are valid.

### `/logout` (GET)
- Logs the user out.
- Requires the user to be logged in (using Flask-Login).

### `/user` (POST)
- Allows a new user to sign up with a username and password.
- Creates a new user in the database.

### `/user/<int:user_id>` (GET)
- Retrieves the profile information of the specified user.
- Requires the user to be logged in.

### `/user/<int:user_id>` (PUT)
- Allows the logged-in user to update their password.
- Users can only update their own information unless they are an admin.

### `/user/<int:user_id>` (DELETE)
- Allows a user to delete their own account.
- Only admins can delete other users' accounts.

## Setup and Installation

1. Clone the repository.
2. Ensure Docker is installed and running to manage the MySQL database.
3. Set up the environment by running `docker-compose up` to start the MySQL container.
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
