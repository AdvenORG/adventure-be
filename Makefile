migrations:
	python  ./manage.py makemigrations
migrate:
	python  ./manage.py migrate
pull_postgres:
	docker pull postgres
run_db_store:
	docker run --name db-store -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
create_admin:
	python  ./manage.py createsuperuser
run:
	python ./manage.py runserver
gen:
	python manage.py generateschema > schema.yml

install:
	poetry add djangorestframework

gcam:
	git add .
	git commit  --amend --no-edit
	git push -f

start:
	python ./manage.py migrate
	python ./manage.py initadmin
	python ./manage.py loadsql
	python ./manage.py runserver 0.0.0.0:8080
