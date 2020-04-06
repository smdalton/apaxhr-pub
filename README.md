# apaxhr
Hr system for apax

Instructions for Dev server

1. git clone
2. cd apaxhr (configure secrets files for aws credentials)

3. python3 rt.py dev_postgres (to run locally with a postgres container)


python3 rt.py dev_on_docker (to run full stack redis/rabbit/celery1&2 locally entirely on containers)
python3 rt.py prod_demo (to run production with RDS database)
