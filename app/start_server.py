import os
import time
import sys

def postgres_message():
    print("*" * 80)
    print("*" +" "* 78 + "*\n")
    print("*" +" "* 78 + "*\n")
    print(' PostGres DB is currently dirty needs to be clean before deployment ')
    print("*" +" "* 78 + "*\n")
    print("*" +" "* 78 + "*\n")

def celery_worker():
    print('Celery worker waiting')
    time.sleep(18)
    os.system('celery -A apaxhr worker --loglevel=info')

def celery_beat():
    print('Celery beat waiting')
    time.sleep(20)
    os.system('celery -A apaxhr beat --loglevel=info  -S django_celery_beat.schedulers:DatabaseScheduler')

def dev():
    # set env's
    os.environ['NUM_USERS']='25'
    os.environ['SQL_ENGINE'] = 'django.db.backends.postgresql_psycopg2'
    os.environ['SQL_NAME'] = 'postgres-dev'
    os.environ['DEV_POSTGRES']='TRUE'
    # os.environ['USE_S3'] = 'TRUE'
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIATWWKT35LU5ED5FDY'
    os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
    os.environ['AWS_STORAGE_BUCKET_NAME'] = 'apaxhr-test'
    os.environ['DEV']='TRUE'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'apaxhr.settings'

    os.system('echo Starting Dev server.')

    ## Configure and initialize database
    os.system('python3 manage.py reset_db --noinput')
    os.system('find . -path "*/migrations/*.py" -not -name "__init__.py" -delete')
    os.system('find . -path "*/migrations/*.pyc"  -delete')
    time.sleep(2)
    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')
    os.system('python3 manage.py migrate django_celery_beat')
    time.sleep(2)
    # populate database
    os.system('python3 manage.py create_users_and_documents')
    os.system('python3 manage.py create_permissions')
    os.system('python3 manage.py create_positions')
    os.system('python3 manage.py create_centers')


    # start webserver
    os.system('python3 manage.py runserver 0.0.0.0:8000 --insecure')
    # os.system('exec gunicorn apaxhr.wsgi:application \
    #         --bind 0.0.0.0:8000\
    #         --workers 3 --reload' )

def prod_server():
    os.environ['DJANGO_SETTINGS_MODULE']='apaxhr.settings'

    os.environ['USE_S3'] = 'TRUE'
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIATWWKT35LU5ED5FDY'
    os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
    os.environ['AWS_STORAGE_BUCKET_NAME'] = 'apaxhr-test'
    os.system('echo Starting Prod server.')
    os.system('python3 manage.py makemigrations')
    os.system('python3 manage.py migrate')
    os.system('python3 manage.py migrate django_celery_beat')
    os.system('python3 manage.py collectstatic --no-input')
    time.sleep(1)

    os.system('exec gunicorn apaxhr.wsgi:application \
        --bind 0.0.0.0:8000\
        --workers 3')


def prod_demo():
    print("sleeping for db")
    time.sleep(5)
    os.environ['DEV_POSTGRES']='TRUE'
    os.environ['USE_S3'] = 'TRUE'
    os.environ['AWS_ACCESS_KEY_ID'] = 'AKIATWWKT35LU5ED5FDY'
    os.environ['AWS_SECRET_ACCESS_KEY'] = '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'
    os.environ['AWS_STORAGE_BUCKET_NAME'] = 'apaxhr-test'
    os.environ['DEV']='TRUE'
    os.system('echo Starting Prod Demo server.')
    # TODO: Reset this for deployment
    # os.system('python3 manage.py collectstatic --no-input')
    os.system('python3 manage.py create_users_and_documents')
    os.system('python3 manage.py create_permissions')


    #os.system('python3 manage.py collectstatic --no-input')
    time.sleep(1)
    os.system('exec gunicorn apaxhr.wsgi:application \
        --bind 0.0.0.0:8000\
        --workers 3')


func_dict = {
    'dev': dev,
    'prod': prod_server,
    'prod_demo': prod_demo,
    'celery_beat':celery_beat,
    'celery_worker':celery_worker,
}


option = sys.argv[1]
valid_options = ['dev','prod','prod_demo','celery_beat','celery_worker']
try:
    assert(option in valid_options)
except:
    print(f"argument not provided / not in valid options: {valid_options} ")

func_dict[option]()




#

# os.system('exec gunicorn apaxhr.wsgi:application \
#     --bind 0.0.0.0:8000\
#     --workers 3')

#python manage.py makemigrations
#python manage.py migrate
##python manage.py collectstatic --no-input
#exec python manage.py runserver