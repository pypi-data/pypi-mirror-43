# Lathorp - PostgreSQL Testing Fixtures

Lathorp provides handy **pytest fixtures** for test code that involves access to a **PostgreSQL** database.

For example, if the code under test writes data to a database, or queries it for data, you want to write tests to see
that it writes and reads the data as you expect.
You need an isolated and controlled environment for testing, so you need to set up a temporary database just for
testing and fill it up with known data.
Setting up a new database is a relatively time consuming operation that slows your tests down. You want to do this
just once per testing session and let multiple tests share the same temporary database instance.
However, many tests should be isolated from each other - you don't want side effects from a test (say, data written to
the database) leaking to another test. The solution is to write known data before each test and delete it all after
the test has finished.


## The Fixtures

The `pg` fixture is a session-scoped fixture that creates a new temporary database once per test session and deletes
it after the session is done.

The `pg_connect` fixture is a function-scoped fixture that you use to establish a connection to the temporary database.
You can optionally load data into the database before the test begins, by pointing to data files that PostgreSQL can
read. The data is automatically deleted after the test function returns, so that it doesn't leak to other tests that
may expect different data.

## Utility Functions

A utility function called `load_schema_definitions` can be used to create the database structure by reading SQL DDL
files that you provide. Embed it in your own session-scoped fixture and call that together with `pg_connect`.

Another utility, `copy_data`, copies data from files in CSV or text format (as supported by PostgreSQL).
It can be used directly, or automatically by passing a path to the files to the `pg_connect` fixture.

A third utility, `delete_data`, deletes all data from a set of tables.
It is used automatically by `pg_connect` to remove data from tables that it loaded with `copy_data`.
You can also use it directly to clean up any changes made by your test.


## Using Lathorp in Your Project

1. Include the `lathorp` package with the development packages of your projects.
With `pipenv`:
```bash
pipenv install --dev lathorp
```

1. Import fixtures from `lathorp` in your tests. You can also import them in `conftest.py` to make them available to all
your tests. See `tests/conftest.py` in this project for an example.

1. Add either `pg` or `pg_connect` as arguments to your test functions, as shown below. There's no point in adding
both, since `pg_connect` itself uses `pg`.
```python
def my_test(pg_connect):
    """A test that connects to the temporary test database."""
    with pg_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 'Hello, world!' AS hello;")
```
For more examples, see `tests/test_fixtures.py` in this project.

1. Lathorp truly shines when you use it together with schema definitions (SQL DDL) files and test data files (CSV or
PostgreSQL-readable text).
Create a session-scoped fixture that calls `load_schema_definitions` and give it the path to your schema definitions.
Then use this fixture along with `pg_connect` and give it the path to your data files.

    ```python
    # In conftest.py
    import pathlib
    from lathorp import load_schema_definitions
    from lathorp.fixtures import pg
    from lathorp.fixtures import pg_connect

    def init_schema(pg):
        load_schema_definitions(pathlib.Path('path/to/my/ddl/file_or_directory'))

    # In your test module
    def test_my_fun(init_schema, pg_connect):
        conn = pg_connect(pathlib.Path('path/to/my_table.csv'))  # loads data into my_table
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM my_table;')
    ```
    Now every test can have access to an initialized database with test-specific data.


## Why "Lathorp?

The name is a reference to [Dr. Emmett Lathorp "Doc" Brown][Emmett Brown on Wikipedia],
the crazy scientist and inventor of the DeLorean time machine from _Back to the Future_ trilogy.

The Lathorp library too lets you go back in time to a fresh database after every test.

[Emmett Brown on Wikipedia]: https://en.wikipedia.org/wiki/Emmett_Brown
