### Overview
Casting Agency is a capstone project for Full Stack Web Developer Nanodegree program. *It doesn't include a frontend.*
Skills needed for this project:
* Coding in Python 3
* Relational Database Architecture
* Modeling Data Objects with SQLAlchemy
* Internet Protocols and Communication
* Developing a Flask API
* Authentication and Access
* Authentication with Auth0
* Authentication in Flask
* Role-Based Access Control (RBAC)
* Testing Flask Applications
* Deploying Applications

### Dependencies
It is recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
Once you have your virtual environment setup and running, install dependencies by running:
```
pip install -r requirements.txt
```
This will install all of the required packages we selected within the requirements.txt file.

### Database Setup
With Postgres running, restore a database using the casting_agency_database.psql file provided. Run the following in a terminal:
```
psql casting_agency_database < casting_agency_database.psql
```

### Running the local server
To export the variables, run:
```
source setup.sh
```

To run the server, execute:
```
flask run --reload
```
The backend will run locally on `http://127.0.0.1:5000/`

### Hosted app
The app is deployed on Heroku.
To access the app, type the following URL in the browser:
```
https://casting-agency-app-21345.herokuapp.com/
```

### API endpoints
<details>
<summary>GET '/actors' - fetches a list of actors.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/actors -H "Authorization: Bearer {TOKEN}"

curl http://localhost:5000/actors -H "Authorization: Bearer {TOKEN}"

```
</details>

<details>
<summary>GET '/movies' - fetches a list of movies.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/movies -H "Authorization: Bearer {TOKEN}"

curl http://localhost:5000/movies -H "Authorization: Bearer {TOKEN}"

```
</details>

<details>
<summary>POST '/actors' - creates a new actor.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"name": "New actor", "age": 45, "gender": "female"}'

curl http://localhost:5000/actors -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"name": "New actor", "age": 45, "gender": "female"}'
```
</details>

<details>
<summary>POST '/movies' - creates a new movie.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"release_date": "Sun, 03 Oct 2021 06:16:21 GMT", "title": "New movie -1234"}'

curl http://localhost:5000/movies -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"release_date": "Sun, 04 Oct 2021 06:16:21 GMT", "title": "New movie - 2"}'
```
</details>

<details>
<summary>PATCH '/actors/:actorId' - updates an actor, specified by id.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/actors/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"name": "Updated Name"}'

curl http://localhost:5000/actors/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"name": "Next Name"}'
```
</details>

<details>
<summary>PATCH '/movies/:movieId' - updates a movie, specified by id.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/movies/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"title": "Updated title"}'

curl http://localhost:5000/movies/1 -X PATCH -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}" -d '{"title": "Next Title"}'
```
</details>

<details>
<summary>DELETE '/actors/:actorId' - deletes an actor.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}"

curl http://localhost:5000/actors/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}"
```
</details>

<details>
<summary>DELETE '/movies/:movieId' - deletes a movie.</summary>

```
curl https://casting-agency-app-21345.herokuapp.com/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}"

curl http://localhost:5000/movies/1 -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}"
```
</details>

### Testing with Unittest
To run the tests, run:
```
dropdb casting_agency_database_test
createdb casting_agency_database_test
psql -f casting_agency_database.psql -d casting_agency_database_test
python casting_agency_database_test
```

### Testing with Postman
* Import the postman collection `casting_agency.postman_collection.json`
* Right-clicking the collection folder for Casting Assistant, Casting Director, and Executive Producer, navigate to the authorization tab, and include the JWT in the token field.
* Run the tests.

### RBAC controls
The app supports the following roles:
* Casting Assistant
    - `get:actors`
    - `get:movies`
* Casting Director
    - `get:actors`, `post:actors`, `patch:actors`, `delete:actors`
    - `get:movies`, `patch:movies`,
* Executive Producer
    - `get:actors`, `post:actors`, `patch:actors`, `delete:actors`
    - `get:movies`, `post:movies`, `patch:movies`, `delete:movies`

### Authentication
This app uses Auth0 for authentication.
Steps to setup Auth0:
* create a new Auth0 Account.
* select a unique tenant domain.
* create a new, single page web application.
* create a new API.
* in API Settings:
    - enable RBAC;
    - enable Add Permissions in the Access Token.
* create new API permissions and roles.