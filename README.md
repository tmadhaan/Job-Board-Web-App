# Tech Job Board

A simple job board web app created using Python and Flask. Users can add, view, search, edit, and delete jobs.

## Features

* View jobs
* Search for jobs by their title
* Add new jobs
* Edit any existing jobs
* Delete jobs
* Store job data using SQLite

## Built With

* Python
* Flask
* Flask-SQLAlchemy
* SQLite
* HTML & CSS

## Running Locally

Clone the repository and install the required packages:

```bash
pip install -r requirements.txt
```

Then run the application:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

## Deployment

This project includes Gunicorn and a `wsgi.py` file so it can be deployed.

