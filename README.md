# ExBanking testing
This Project is used for test automation purposes of ExBanking app.
Project was created to show basic structure, not for being used as a framework for production system.

### Virtual environment
Project uses `pipenv` as a packaging tool for Python.

1. Install `pipenv` globally: `pip install pipenv`

2. Create virtual environment: `pipenv shell`

If you use `PyCharm` it can be created manually through `Interpreter Settings`

3. Install dependencies in virtual environment: `pipenv install`

### Application
Application API is stored in the app.py file in root. You could use and run it from local or use docker virtualization for it: 

`docker build -t exbanking_app .` - to build docker container 

`docker run -d -it -p 5005:5005 exbanking_app ` - to run app in the docker 

## Local running
### API tests
`pipenv run pytest api_tests/tests_ex_banking.py` - run all api tests and save results to test_report folder

### Running tests with specific Groups
By default, all tests would run. Tests can have one or more marks. Marks should be declared in `*.ini` file. You could run 
just specific group of tests used '-m' parameter, e.g.

`pipenv run pytest api_tests/tests_ex_banking.py -m "api and regression"`

### Test report tool
Project use Allure Framework as a flexible lightweight multi-language test report tool.

More info: [allure docs](https://docs.qameta.io/allure/)

#### For generating report after local run: 

`pipenv run allure serve tests_report`

### Performance tests tool
Project use a Locust as an open source load testing tool. For run performance test tool: 

`locust -f performance_tests/test_perf_api.py`
