# University-Campus-Portal-UCP
Free &amp; Open source Web application for Universities

## Installation Instructions
1. Create a new virtual environment for the project
2. Install required python libraries giving in the requirements.txt file
   
    ```bash
    pip install -r requirements.txt
    ```
3. Create a file named settings_local.py in the same location as the projects settings.py file
4. Add your local database details to the settings_local.py file

    ```python
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_user_name',
        'PASSWORD': 'your_mysql_user_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
    ```
5.  Add SMTP details to the settings_local.py file

    ```python
EMAIL_USE_TLS = True
EMAIL_HOST = 'your_smtp_host'
EMAIL_HOST_USER = 'your_smtp_username'
EMAIL_HOST_PASSWORD = 'your_smtp_password'
EMAIL_PORT = your_smtp_port_number
    ```
6.  Other Settings you can choose to personalize the portal are SITE_TITLE, LOGO and THEME

    ```
7. Run python migrations.
    
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
