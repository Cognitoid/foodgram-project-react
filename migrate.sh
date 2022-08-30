cd /e/Dev/foodgram-project-react/
source venv/Scripts/activate
cd /e/Dev/foodgram-project-react/backend/
alias python='winpty python.exe'
python manage.py makemigrations api recipes users
python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@admin.ru', 'admin')" | python manage.py shell
python manage.py load_ingredients