# apaxhr
Hr system for apax

Instructions for Dev server

git clone repo
configure secrets files for aws credentials

to run locally with a postgres container:
python3 rt.py dev_postgres

to run locally entirely on containers:
python3 rt.py dev_on_docker

to run production with RDS database
python3 rt.py prod_demo
