##Dockerizing Flask Boilerplate

###Specification
 - Docker
 - Docker-Compose
 - Flask (python 3)
 - Nginx
 - Postgresql
 - Redis

##Folder Structure

    Main
     |--- /nginx
     | |--- Dockerfile
     | |--- /logs    
     | |--- /ssl
     | |--- /sites-enabled
     | | |--- nginx_all
     | | |--- nginx_with_ssl
     | | |--- nginx_with_ssl_only
     | | |--- nginx_without_ssl     
     |--- /web
     | |--- Dockerfile
     | |--- manage.py
     | |--- requirements.txt
     | |--- tests
     | |--- /project
     | | |--- __init__.py
     | | |--- config.py
     | | |--- /templates 
     | | |--- /static
     | | |--- apps
     | | | |--- __init__.py
     | | | |--- models.py
     | | | |--- forms.py
     | | | |--- views.py
     | | | |--- /templates
     |--- .env
     |--- docker-compose.yml
     |--- README.md

###Install/Configure Docker

    $ curl -sSL https://get.docker.com/ | sh
    $ pip install docker-compose

###Create ".env" file on the Main Folder - this file contains all OS level environment variables ()
    
    #sample .env file
    DEBUG=False
    SECRET_KEY=secret_key
    DB_NAME=postgres
    DB_USER=postgres
    DB_PASS=postgres
    DB_SERVICE=postgres
    DB_PORT=5432
    DEBUG_TB_ENABLED=False
    THEME_VERSION=4.5.4  
    APP_SETTINGS=project.config.ProductionConfig  
    NOTEBOOK_PASSWORD='sha1:0c80a71d63da:a1ca534342f6cdbe8e71c80f06f1fcc0011bd55b'    

###Create SSL

    Soon
    
###Configuration

    # Change postgres password (Security Reasons), Add User for the application
    $ psql -h 127.0.0.1 -p 5432 -U postgres --password
    postgres=# ALTER USER postgres WITH PASSWORD 'desired_password';
               CREATE DATABASE web;
               CREATE USER web WITH PASSWORD 'test';
               GRANT ALL PRIVILEGES ON DATABASE "web" to web;

    $ docker-compose run web /usr/local/bin/python manage.py create_db

###Postgres Backup

    $ docker exec -it suite_postgres_1 \
      sh -c "pg_dump -U postgres_user postgres_dbname | gzip > /postgres/backup/dump_`date +%d-%m-%Y"_"%H_%M_%S`.gz"

###Postgres Restore

    $ docker exec -it suite_postgres_1 \
        sh -c "gunzip -c /postgres/backup/filename.gz | psql -U postgres_user postgres_dbname"

###Execute Raw sql with flask-SqlAlchemy
    
    from project import db
    db.engine.execute("ALTER SEQUENCE team_tasks_id_seq RESTART WITH 2001;")

###Create /.env for environmental variables

    DEBUG=False
    SECRET_KEY=5(15ds+i2+%ik6z&!yer+ga9m=e%jcqiz_5wszg)r-z!2--b2d
    DB_NAME=web
    DB_USER=web
    DB_PASS=test
    DB_SERVICE=postgres
    DB_PORT=5432

    APP_SETTINGS=project.config.ProductionConfig

###sample merging for pandas for data analysis
    
    from project.models import User, UserGroup
    import pandas as pd
    
    from collections import defaultdict
    from sqlalchemy.inspection import inspect
    
    def query_to_dict(rset):
        result = defaultdict(list)
        for obj in rset:
            instance = inspect(obj)
            for key, x in instance.attrs.items():
                result[key].append(x.value)
        return result
    
    user = User.query.join(UserGroup).filter(UserGroup.id == 1).all()
    user_group = UserGroup.query.all()	
    
    df_user	= pd.DataFrame(query_to_dict(user))
    df_usergroup = pd.DataFrame(query_to_dict(user_group))
    
    # pd.merge(left, right, left_on='group_id', right_on='id', how='inner', indicator=True)
    
    # how must be inner if you want to filter and remove unrelated items
    # how must be outer if you want to create rows even if no common in relational keys
    
    merged = pd.merge(df_user, df_usergroup, left_on='group_id', right_on='id', how='inner', indicator='indicator_column')
    


###Handy Snippets

- KILL ALL DOCKER CONTAINER


    $ docker kill $(docker ps -a -q)

- REMOVE ALL DOCKER CONTAINER


    $ docker rm $(docker ps -a -q)

- LIST ACTIVE SERVICES


    $ netstat -tuplen

###Deployment Note
    git clone -b <branch> <repo> <foldername>
    copy .env to the Host
    copy SSL Certs
    copy static files
    update DB

###References
* <https://docs.docker.com/installation/centos>
* <http://containertutorials.com/docker-compose/nginx-flask-postgresql.html>
* <https://realpython.com/blog/python/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud>
* <https://realpython.com/blog/python/docker-in-action-fitter-happier-more-productive>
* <https://github.com/sameersbn/docker-postgresql>
* <http://www.postgresql.org/docs/8.0/static/sql-alteruser.html>
* <https://hub.docker.com/r/eeacms/postgres>