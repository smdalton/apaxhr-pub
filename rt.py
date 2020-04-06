#!/usr/bin/env python

import os, sys
import time

"""
Run tools help
"""
env_flags = ['DEV', 'DEV_REDIS', 'DEV_NGINX', 'DEV_REDIS_NGINX', 'PROD','SERVE_STATIC', 'USE_S3']

def clear_envs():
    for env in env_flags:
     try:
        os.environ.pop(env)
     except:
         print(env, "Not set")

def start_rabbit():
    rabbit_start = 'docker run -d --hostname my-rabbit' \
                   ' --name anony-rabbit' \
                   ' -p 15672:15672 -p 5672:5672' \
                   ' rabbitmq:3-management'
    os.system(rabbit_start)


def start_postgres():
    print('Starting Postgres')
    time.sleep(.5)
    postgres_start = 'docker run -d -p 5432:5432 --name postgres-dev' \
                     ' -e POSTGRES_PASSWORD=pass1234' \
                     ' -e POSTGRES_USER=postgres-dev ' \
                     'postgres'
    os.system(postgres_start)

def stop_postgres():
    print('Stopping Postgres')
    postgres_stop = 'docker kill postgres-dev'
    os.system(postgres_stop)

def delete_postgres():
    print('Deleting Postgres')
    postgres_delete = 'docker container rm postgres-dev'
    os.system(postgres_delete)



def kill_services():
    print("killing services")
    stop_postgres()
    time.sleep(1)
    delete_postgres()


# TODO: Run server with DEV sqlite db and no server_nginx or redis
def dev_postgres():
    kill_services()
    clear_envs()
    start_postgres()
    os.chdir('app')
    os.system('python3 start_server.py dev')


def dev_on_docker():
    os.system('docker container rm postgres-dev')
    os.system('docker-compose -f docker-compose.dev.yml build')
    os.system('docker-compose -f docker-compose.dev.yml up')


def prod_demo():
    os.system('docker-compose -f docker-compose.demo.yml build')
    os.system('docker-compose -f docker-compose.demo.yml up')
    print("running prod no services")

# TODO:

def deploy_test():
    start_postgres()
    os.chdir('app')
    os.system('pytest --cov=. ')

function_dict ={
    'dev_postgres': dev_postgres,
    'dev_on_docker': dev_on_docker,
    'prod_demo': prod_demo,
    'deploy_test': deploy_test,
}

try:
    option = sys.argv[1]
    print(f"Running {option}")
    function_dict[option]()
except:
    print([key for key in function_dict.keys()])
finally:
    kill_services()
    print('Execute cleanup code here')
