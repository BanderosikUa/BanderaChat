# Database Configuration

This is an internal documentation for the database configuration of a FastAPI project that uses MySQL, SQLAlchemy, and Alembic migrations.

## Configuration

The `DATABASE_URL` is configured in the `src.config` file using environment parameters for the database username, password, host, socket, and name.

A session local object is created using the sessionmaker function.

A `Base` object is created using the declarative_base function from SQLAlchemy. This will be used for defining database models.

The `get_db` function creates a new database session, yields the session object, and then closes the session after it's done being used.

Finally, a custom `BinaryUUID` type decorator is defined to optimize UUID keys by storing them as 16 bit binary and retrieving them as UUID. This decorator works only for MySQL DB. For Postgres, use `from sqlalchemy.dialects.postgresql import UUID`.

## Alembic

In the `base.py` file, we import the `Base` object and all the project models, which will make it easier for Alembic to detect the changes and autogenerate the migrations.

The `env.py` file in Alembic imports `Base` from the `base.py` file and sets the `target_metadata` variable to `Base.metadata`.


## Test database

In this project, a test MySQL database is created for Pytest by using a SQL entrypoint and Docker Compose.
```
volumes:
    - ./entrypoints/mysql:/docker-entrypoint-initdb.d
```
This allows for automated testing of the database functionality without interfering with the development or production databases. The test database is automatically created and destroyed with each test run.
