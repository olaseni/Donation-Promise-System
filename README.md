#### Donation Promise System

The _Donation Promise System_ is a Django app simplistically similar to the basic context of a donations fund.
People get to make contributions in donation promises toward a cause.

##### Minimum Requirements

- Docker/docker-compose
- Python 3.6+
- Django 2.1
- Postgresql
- Redis
- Make (DevOps only)

The app ships with a `requirements.txt` file that contains other python dependencies that can be installed via `pip`.

It also depends on __make__ and `Makefiles` to ensure that all commands are in one place.


##### Building

The app needs an initial context to be setup. Running `make build` for the first time will ensure that docker pulls
all images and that Django runs the initial migrations. Demo-data will also be injected into the db.

    $> make build
    
`make build` incorporates three commands: `make run`, `make manage-migrate`, `make manage-demodata`

##### Running

The app can be started by running: 

    $> make run

##### Tests

Tests can be run: 

    $> make lint-and-test
    
#### Coverage

Run tests coverage

    $> make lint-and-test-and-coverage

##### Demo Data

Demo data can be created: 

    $> make manage-demodata