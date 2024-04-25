# Blog_Webapp
Simple blog application as assessment task for Django.
In blog app, non logged-in users can view posts and authors. Authors are able to create blog posts and comment on others post.

## Installation
1. Clone the repository
```bash
git clone https://github.com/nidhi-tagline/Blog_Webapp.git
```

2. Navigate to project directory
```bash
cd Blog_Webapp
```

3. Create a virtual environment and activate it
```bash
python -m venv env
source env/bin/activate
```

4. Install the Dependencies:
```bash
(env)$ pip install -r requirements.txt
```

5. Make migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Runserver
```bash
python manage.py runserver
```

7. Open http://localhost:8000/blogs in your browser
