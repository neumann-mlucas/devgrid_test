
### INSTALATION
```sh
$ git clone https://github.com/neumann-mlucas/devgrid-test
$ pipenv install
```

### RUN DEVELPMENT VERSION
```sh
$ pipenv run flask run
```

### CONFIG
write a .venv file in the project's root directory
variables:
- FLASK_APP : temperature_api.py
- DEBUG : True or False
- API_KEY : your Weather API key
- CACHE_TTL : lifetime of cache items in seconds
- DEFAULT_MAX_NUMBER : default max number of items returned by '/temperature' endpoint

### RUN TEST
```sh
$ pipenv  run pytest
```

### API CALL EXAMPLES
```sh
$ curl http://127.0.0.1:5000/temperature
$ curl http://127.0.0.1:5000/temperature/brasilia
```
