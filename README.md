# 🎬 Cinescope

Cinescope is a movie review platform built with Django that allows users to discover, review, and rate movies. It features user authentication, a custom admin dashboard, and a responsive UI designed for a seamless movie community experience.

## 🚀 Features

- User registration and login system  
- Add, edit, and delete movie reviews  
- Star ratings and review statistics  
- Search and filter by title, genre, or rating  
- Custom admin dashboard for managing content  
- User profiles with review history  
- Fully responsive design  

## 🛠 Tech Stack

- Frontend: HTML, CSS, Bootstrap  
- Backend: Python, Django  
- Database: SQLite (default), PostgreSQL/MySQL optional  
- Others: Django Templates, Django Forms  

## 💻 Getting Started

### 1. Clone the Repository

```
git clone https://github.com/your-username/cinescope.git
cd cinescope
```

### 2. Create and Activate Virtual Environment

```
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

`

### 3. Apply Migrations

```
python manage.py migrate
```

### 4. Run the Development Server

```
python manage.py runserver
```

Open your browser and go to `http://127.0.0.1:8000/`

## 🔐 Admin Access

To access the admin panel:

```
python manage.py createsuperuser
```

Then visit: `http://127.0.0.1:8000/admin/`


## 🚀 Deployment

You can deploy this project on platforms like:

- Render  
- Railway  
- Heroku (with PostgreSQL)

Make sure to:

- Set `DEBUG = False`  
- Configure `ALLOWED_HOSTS`  
- Store `SECRET_KEY` securely using environment variables  

## 🙋‍♂️ Author

**Kushal Narendracumar**  
GitHub: [https://github.com/Kushal-Narendracumar7](https://github.com/Kushal-Narendracumar7)  
Email: kushalbamania7@gmail.com

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)

## 💡 Future Improvements

- REST API support  
- Social login (Google, GitHub)  
- Review like/upvote system  
- Personalized movie recommendations  
- Dark mode
