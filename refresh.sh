function print_header() {
    echo -e "\n******* ${1} *******"
}

print_header "Deleting existing files"
rm app/migrations/0001_initial.py
rm db.sqlite3

print_header "Executing 'Make migrations'"
python manage.py makemigrations

print_header "Executing 'Migrate'"
python manage.py migrate

print_header "Executing 'Sql migrate'"
python manage.py sqlmigrate app 0001

print_header "Register superuser"
python manage.py createsuperuser
