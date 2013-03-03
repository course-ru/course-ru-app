virtualenv venv --distribute
source venv/bin/activate
pip install -r requirements.txt
./manage.py syncdb --noinput
./manage.py loaddata fixtures/admin.json
./manage.py runserver
