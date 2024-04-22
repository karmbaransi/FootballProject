pip install selenium
pip install termcolor
pip install webdriver_manager
python manage.py makemigrations
python manage.py migrate
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -f
dpkg -i google-chrome-stable_current_amd64.deb
python manage.py runserver
