sudo pip install virtualenv
virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
./manage.py syncdb
./manage.py runserver
