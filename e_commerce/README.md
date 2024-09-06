Setup Instructions
Step 1: Create a Virtual Environment:
assessment > python -m venv env

Step 2: Activate the Virtual Environment:
assessment > source env/bin/activate

Step 3: Install Dependencies:
assessment/e_commerce > pip install -r requirements.txt

Step 4: Create Database Tables:
assessment/e_commerce > python manage.py migrate

Step 5: Load Data into Database:
assessment/e_commerce > python manage.py upload_data_from_csv

Step 6: Test API: Use the provided API collection and environment details sent via email.
    Run API Endpoints:
        Registration: {{base_url}}/signup/
        Login: {{base_url}}/login/
        Get Summary Report: Authenticated with JWT Token (obtained from the login API) - {{base_url}}/summary-report/
