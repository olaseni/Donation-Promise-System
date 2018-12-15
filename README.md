#### Donation Promise System

The _Donation Promise System_ is a Django app simplistically similar to the basic context of a donations fund.
People get to make contributions in donation promises toward a cause.

##### Minimum Requirements

- Docker/docker-compose
- Python 3.6+
- Django 2.1
- Postgresql
- Redis

The app ships with a `requirements.txt` file that contains other python dependencies that can be installed via `pip`

##### Running

The app can be started by running: 

    $> make start

##### Tests

Tests can be run: 

    $> make lint-and-test
    
#### Coverage

Run tests coverage

    $> make lint-and-test-and-coverage

##### Demo Data

Demo data can be created: 

    $> make manage-demodata