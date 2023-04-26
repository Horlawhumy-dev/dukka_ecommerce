# Dukka Power Backend Test


### Local Setup

- Clone the repository with ` git clone git@github.com:Horlawhumy-dev/dukka-power-test.git`
- Navigate to `dukka-power-test directory and activate virtual environment based on your os using command below
- Note: If you do not have `development` branch after cloning, then run the command below;
- Run `git fetch origin development`
- Make your feature branch with command ` git checkout -b <your_feature_branch> origin/development` .
- Run `python3 -m venv venv` Then activate the environment
- If windows? Run `source venv/Scripts/activate`
- If Mac/Linux Run `source venv/bin/activate`.
- Run `pip install -r ./dukka_ecommerce/requirements.txt` for installing requirements.
- Copy everything from `env.example` to `.env` file and edit accordingly.
- Run `python3  ./dukka_ecommerce/manage.py makemigrations` and `python3 ./dukka_ecommerce/manage.py migrate` to migrate model to db.
- Run `pytest` for tests.
- Lastly, Run `python3 ./dukka_ecommerce/manage.py runserver` to spin up server locally.


#### Do not hesitate to reach out by creating an issue if there is any problem.
#### Note: Never run the command `pip freeze > requirements.txt` because it copies unneccessary dependencies from virtual env.

### Happy Coding
