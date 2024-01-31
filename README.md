## Table of Contents

- [Project Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description
This is a Library Management System API project made using FastAPI and Postgres.
This project consists of 4 database models which are users, books, books_details and borrowed_books model.

## Installation
Before installing the project your system must have python and pip installed.

To install the project, run the following command:
1. Clone the project 
2. In root directory create .env file and put your database credentials as required
3. Make virtual environment using `py3 -m venv venv`
4. Activate virtual environment using `Source venv/Scripts/activate`
5. Install the project dependencies using `pip install -r requirements.txt`


## Usage
1. Change the working directoy to app
2. Now run the project using `uvicorn main:app --reload`
3. Navigate to `localhost:8000/docs` for swagger API documentation to interact with the API
