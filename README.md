Getting the database running with docker:
1. Change the database in settings.py and docker-compose.yml
2. Add a .env in the same directory as the docker-compose.yml
3. Change the directory to the same directory as the docker-compose.yml && docker compose up
4. If you have any issues, double-check the container names/check the errors
5. Once the docker container is running, execute this from the same directory as the docker-compose.yml
6. docker compose exec web python manage.py makemigrations && docker compose exec web python manage.py migrate
7. Copy database files - docker cp ./bluevoyagedb_backup.sql db_server:/docker-entrypoint-initdb.d/
8. Dump database files - docker exec db_server pg_dump -U postgres bluevoyagedb > bluevoyagedb.sql