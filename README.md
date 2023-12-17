# Kami Airlines API

### Endpoint: /api/v1/aircraft [POST]
```
{
  "airplane_identifier": 10,
  "passenger_capacity": 300
}
```
Adds one aircraft to the aircraft fleet.
- We have only 10 types of aircraft [2,3,4,5,6,7,8,9,10,11]
- "airplane_identifier" must be from 2 to 11

### Endpoint: /api/v1/aircraft/{identifier} [GET]

Generates specifications for a specific aircraft.
- Fuel consumption per minute
- Maximum minutes able to fly

### Installation and Application Launch Process
```
cd kami
virtualenv --python=python3.11 env
. env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### OpenAPI Documentation
```
http://localhost:8000/api/docs
```

### Running Tests
```
python manage.py test
```

### Running Linters
```
make linters
```