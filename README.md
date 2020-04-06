# Apax English ERP and document mangement tools
### Hr system for apax

### Quickstart

1. git clone
2. cd apaxhr (configure secrets files for aws credentials)
### Select the desired configuration
3. python3 rt.py dev_postgres (to run locally with a postgres container)
4. python3 rt.py dev_on_docker (to run full stack redis/rabbit/celery1&2 locally entirely on containers)
5. python3 rt.py prod_demo (to run production with RDS database)
