# PRiSM
Process Reporting in System macOS

### Python Installation (Development)
1.  Clone this repository into your desired directory
2.  Create a venv for your project and install required files
    -   `pip3 install pipenv`
    -   `pipenv --python 3.9.1`
    -   `pipenv install --dev`
    -   `pipenv run pre-commit install -t pre-commit`
    -   `pipenv shell`

### Python Installation (Production)
We will need to setup pipenv as part of the build when the app is installed.

This would require something like the following commands
-   `pip3 install pipenv`
-   `pipenv --python 3.9.1`
-   `pipenv install`

Then, to run the backend:
-   `pipenv run python backend`
