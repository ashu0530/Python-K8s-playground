# User-Driven Kubernetes Resource Provisioning Service
This is a Flask-based web application designed to interact with a Kubernetes cluster. The application allows authenticated users to dynamically create and manage Kubernetes resources such as Pods, Services, and Ingresses. The application also uses Redis for session management.

## Features

- **User Authentication**: Secure user login and session management using Flask-Login and Flask-Session.
- **Kubernetes Resource Management**: 
  - Create Nginx Pods, Services, and Ingresses within a specified Kubernetes namespace.
  - Automatically assign unique names to resources and manage their lifecycle.
  - Clean up resources (Pods, Services, Ingresses) upon user logout.
- **Redis Integration**: 
  - Store and manage session data in Redis.
  - Ensure that users can only have one active session at a time.
- **Dynamic Ingress Management**: 
  - Generate unique Ingress URLs for accessing the deployed Nginx pods.

## Requirements

- Python 3.7+
- Flask
- Flask-Login
- Flask-Session
- Redis
- Kubernetes Python Client (`kubernetes` package)
- WTForms
- SQLite (or another SQLAlchemy-compatible database)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/flask-k8s-management.git
   cd flask-k8s-management
   ```

2. **Create a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Configure the application:**

   - Modify the `SECRET_KEY` in the `app.config` to a secure key.
   - Update the `SQLALCHEMY_DATABASE_URI` to point to your database.
   - Set the `custom_kubeconfig_path` to the path of your Kubernetes configuration file.
   - Ensure that Redis is running on `localhost` (or update the Redis configuration if it's hosted elsewhere).

6. **Run the application:**

   ```bash
   flask run --host=0.0.0.0 --port=80
   ```

## Usage

### Create an Nginx Pod

1. **Login** to the application.
2. Navigate to `/create` and enter the desired Pod name.
3. The application will create a new Nginx Pod, Service, and Ingress in the Kubernetes cluster.
4. You will be redirected to the Ingress URL to access the Nginx service.

### Logout and Cleanup

1. **Logout** of the application.
2. The application will automatically delete the associated Kubernetes resources (Pod, Service, Ingress) and clean up the session data in Redis.

## Project Structure

- `app.py`: Main application file that sets up the Flask app, routes, and Kubernetes interactions.
- `auth.py`: Handles user authentication, registration, and session management.
- `templates/`: Contains the HTML templates used for rendering the web pages.
- `static/`: Contains static files (CSS, JS, images).
- `database.db`: SQLite database file (or other database if configured).

## Security Considerations

- **Secret Key**: Make sure to set a strong secret key in `app.config['SECRET_KEY']`.
- **User Authentication**: Ensure proper user authentication and session management to prevent unauthorized access.
- **Kubernetes Access**: The application uses a Kubernetes config file. Ensure that the Kubernetes credentials have appropriate permissions and are kept secure.


- Replace `your-username` with your actual GitHub username or appropriate repository URL.
- Adjust the installation steps, paths, and configurations based on your actual setup.
- The `LICENSE` file should be included if you want to distribute your project with an open-source license like MIT.

This `README.md` provides an overview of the application, instructions for setting it up, and other relevant information to help others understand and use your project.
