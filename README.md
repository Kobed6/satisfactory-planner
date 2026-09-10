# Set up

## Creating a Virtual Environment + Installing Dependencies

With the project root as the current directory, run

```
python -m venv .venv
```

Install dependencies with

```
pip install -r requirements.txt
```

On MacOS, activate the virtual environment using

```
source .venv/bin/activate
```

On Windows, use

```
./venv/Scripts/activate
```

To deactivate the virtual environment, run

```
deactivate
```

## Initializing the Database

Download and install MySQL.  
In a bash terminal, enter

```
mysql -u root -p
```

Enter your MySQL password to connect to MySQL's command line interface. Then, enter

```
CREATE DATABASE (database name);
```

It should return Query OK...

### Environment File

Create a .env file in the project root folder with the following variables:

```
DB_HOST = (Your database host, localhost for running locally)
DB_PORT = (Your database port, 3306 by default)
DB_USER = (Your MySQL user, root by default)
DB_PASSWORD = (Your MySQL password)
DB_NAME = (Your database name)
```

With your virtual environment active, run the init_db.py file. For example, by running in the project root folder:

```
python backend/src/init_db.py
```

## Running Web Application

First, go into the frontend directory. Then, run

```
npm i
```

Run the application using

```
npm run dev
```

The application will likely run on localhost:5173

For the backend, on a separate terminal, run

```
uv run fastapi dev backend/src/main.py
```
