@ECHO OFF
REM "Compiles" the project using established tooling and starts the server

REM Run the ruff linter over python
uv run ruff check

REM Run tsc for typescript files in app/static/ts/*.ts


uv run flask run