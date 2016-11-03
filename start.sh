source pypy_venv/bin/activate
source db.sh
export FLASK_APP=search.py
flask run --host=0.0.0.0 --port=80
