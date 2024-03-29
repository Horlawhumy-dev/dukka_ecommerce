### Local Setup

- Clone the repository with ` git clone git@github.com:Horlawhumy-dev/dukka_ecommerce.git`
- Navigate to the directory and activate virtual environment based on your os using command below
- Note: If you do not have `development` branch after cloning, then run the command below;
- Run `git fetch origin development`
- Make your feature branch with command ` git checkout -b <your_feature_branch> origin/development` .
- Run `python3 -m venv venv` Then activate the environment
- If windows? Run `source venv/Scripts/activate`
- If Mac/Linux Run `source venv/bin/activate`.
- Run `pip install -r requirements.txt` for installing requirements.
- Copy everything from `env.example` to `.env` file and edit accordingly.
- Run `python3  manage.py makemigrations` and `python3 manage.py migrate` to migrate model to db.
- Run `pytest` or `python3 manage.py test` for tests.
- Lastly, Run `python3 manage.py runserver` to spin up server locally.



### CELERY Tasks CONFIG

Note: You can as well follow this [article](https://www.nickmccullum.com/celery-django-periodic-tasks/) for the celery configuration.

Then, these commands could be run in separate terminal to see payment reoccurrence in acction.

- Run `celery -A dukka_ecommerce worker --loglevel=info` to start worker

- Run `celery -A dukka_ecommerce  beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler` to start scheduler beat

- Run `kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n'  ' ') > /dev/null 2>&1` to kill any celery task running

- Run `pkill -f "celery worker"` to kill running worker

- Run `celery -A dukka_ecommerce beat -l info --logfile=celery.log --detach` to create new worker log file

- Run `celery -A dukka_ecommerce beat -l info --logfile=celery.beat.log --detach` to create new scheduler beat log file



### Postman Collections
These are the links to the published Endpoints for the test.

[Account Auth](https://documenter.getpostman.com/view/18546780/2s93eSXZya) \
[Payment History](https://documenter.getpostman.com/view/18546780/2s93eSXa45) \
[Payment](https://documenter.getpostman.com/view/18546780/2s93eSXa46)

#### Note: Never run the command `pip freeze > requirements.txt` because it copies unnecessary dependencies from the virtual environment. Instead, use `pip chill` or manually add any installed dependencies into `req.txt`.
