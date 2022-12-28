# simple-secret-manager
This is an example project, DO NOT USE this application or code in production enviroment. This application propose a method to share secrets in a CI/CD enviroment. The project has not been tested or optimized so expect misbehaviours.

## Configure and run
--------------------
Create a virtual env and install dependencies (Recomended version Python 3.10.x)
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install requirements.txt
```
This project user sqlite3 for development purposes
```
$ cd ssmanager
$ python ./manage.py makemigrations
$ python ./manage.py migrate
```
Create Django superuser
```
$ python ./manage.py createsuperuser
```
Run server on `http://localhost:8000/`
```
$ python ./manage.py runserver
```

## How to use
Go to `http://localhost:8000/register` an register an account.

Generate a 1024bits RSA key pair for your service. You can use the following examples for testing.

Public key:
```
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChXc+ZvgY8ElRWjDORJYJ6W3eCwZD4U5fNOJa2zPS+CyV47LDOI7SBZidiEGqZabDVq4uYvHXEq5QltOIlyhp8J7RxzatNKNmqTxE1tN6IYW4VMpEqwoY4FaSOEFfohuzX11XNxX9FMwOXCwmmxahKyb+QmWn8cyPcwzzAaHciaQIDAQAB
```

Private key:
```
MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAKFdz5m+BjwSVFaMM5Elgnpbd4LBkPhTl804lrbM9L4LJXjssM4jtIFmJ2IQaplpsNWri5i8dcSrlCW04iXKGnwntHHNq00o2apPETW03ohhbhUykSrChjgVpI4QV+iG7NfXVc3Ff0UzA5cLCabFqErJv5CZafxzI9zDPMBodyJpAgMBAAECgYAKTAgxUVTohGrpUuz/eBtJX4jSyTNNBViMee30IEQF1IRBoSjvHowoLbKZqV6EB6CHIfk4d94z/JbpiQ9dRfZGl/NgFTUXuAWhyHgr1iDRCAIVQh05/aDOCB5FrsoAWHBoLE+eUIfGLYou0REOIiGbIziucVoQfPmaSl+8p7n+2QJBANQvY8Cz6DGnxaSn7sCNHdUBGthforheLcihzKTjgzlEYdacf+Dt72eC0VZ0ACUvxKCdoQgz0N827a8JdycXfqMCQQDCsAaL+eihqAyxoyrmUjPFp4tL9kTlYP2iU1OJGhiDW8hamY6GyASLNJlukBFvZH2KOu6V9I7N85cNtbujJ6eDAkA4cerdZn6MRw9CwBG5U1DuSv7zNG27EgKn7rLb4lIUN+a3CqbSFTmslZZOo0kum0h5WbVu0ynrV1dfSutRkOR1AkAJclke+aVcErdq9yvhuSNh99s+eFineKlV8w0enfGKji2Ol9zelV4DEy5OuxbdfNbKmklxZUh4ndU6iRLtu8LZAkB4I7FHlI19lBMQFzUCcqNjasWgeKDGd/+99FZrjpDMyt8PF8rvgD/DpIeBm5K0NezSHNMKOm7N6liI56vSx8Ef
```

Generate a RSA symmetric key. Can use the following example for testing.

Symmetric key:
```
4428472B4B625065
```

All key strings must be suitable for base64 encoding.

Go to `http://localhost:8000/create`, introduce the public key, symmetric key and secrets. Secrets must be introduced following the pattern:
```
[{"name":"secret_1","value":"value_1"},{"name":"secret_2","value":"value_2"},...{"name":"secret_n","value":"value_n"}]
```
Once the create button is pressed secrets will be stored. You can access them going to `http://localhost:8000/list` and using the private service key.

## (EXAMPLE) Retrieve secrets and configure .env file
-----------------------------------------------------

Secrets can be retrieved via API request `http://localhost:8000/api/secrets/list`. The following scripts takes 3 arguments (server url, service id, private service key) and create a `.env` file with all the secrets retrieved.

```
#!/bin/bash

url="$1"
service_id="$2"
priv_key="$3"

output=$(curl --location --request POST "$url" --form "priv_key=$(printf "%q" "$priv_key")" --form "service_id=$(printf "%q" "$service_id")")

input="$output"

output=$(echo "$input" | jq -r '.secrets[] | "\(.name)=\(.value)"' | awk -F '=' '{print $1 "=" $2}')

script_dir=$(dirname "$0")

echo "$output" > "$script_dir/.env"

exit 0
```
