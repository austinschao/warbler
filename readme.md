<div id="top"></div>


<!-- ABOUT THE PROJECT -->
# Flask Warbler (Twitter Clone)
## Python - Flask - SQLAlchemy

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python](https://docs.python.org/3/)
* [Flask](https://flask.palletsprojects.com/en/2.1.x/)
* [Flask-SQLALchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Warbler is a full stack application that allows users to follow other users, post messages about their day, and like other posts.


### Installation

Prior to installing all of the requirements, create a venv folder and install the requirements inside of there:

    $ python3 -m venv venv


To activate the venv:

    $ source venv/bin/activate


To install all of the requirements from `requirements.txt`

    $ pip3 install -r requirements.txt


<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

Insert dummy data into a Postgres database from the Mac terminal:

    $ psql (Activates PSQL if it's already been installed)

    CREATE DATABASE warbler; (Creates database for Warbler dummy data)
    CREATE DATABASE warbler_test; (Creates databasea for Warbler test data)

    Control-D (exits PSQL)

Create .env file with the following information:

    Set your own secret key:
        for example, SECRET_KEY=abc123

    DATABASE_URL=postgresql:///warbler


Inside of the root directory, seed the database with dummy data for Warbler:

    $ python3 seed.py

To run tests:

    $ python -m unittest test_message_model.py
    $ python -m unittest test_user_model.py
    $ python -m unittest test_message_views.py
    $ python -m unittest test_user_views.py

To run the server:

    $ flask run -p 5001



<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

Ideas for improving the current setup

- Look into blueprints for separation of routes from app.py
- Add additional tests
- Add additional CSS for styling

<p align="right">(<a href="#top">back to top</a>)</p>


# Made by Austin Chao

<p align="right">(<a href="#top">back to top</a>)</p>

