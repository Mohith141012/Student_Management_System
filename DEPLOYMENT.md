# Deployment Guide - Student Management System

## Option 1: PythonAnywhere (Recommended for Beginners)

### Free tier includes:
- Python web app hosting
- MySQL database (200MB)
- HTTPS enabled
- Custom domain support

### Steps:

1. **Create account at [PythonAnywhere](https://www.pythonanywhere.com)**

2. **Upload your code:**
   ```bash
   # On PythonAnywhere Bash console
   git clone https://github.com/yourusername/Student-Management-System.git
   cd Student-Management-System
   ```

3. **Create virtual environment:**
   ```bash
   python -m venv sms
   source sms/bin/activate
   pip install -r requirements.txt
   ```

4. **Set up MySQL database:**
   - Go to "Databases" tab
   - Create a new database (e.g., `yourusername$sms`)
   - Note the hostname, username, password
   - Import your schema:
   ```bash
   mysql -h yourusername.mysql.pythonanywhere-services.com -u yourusername -p yourusername$sms < sms_data.sql
   ```

5. **Configure web app:**
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code directory: `/home/yourusername/Student-Management-System`
   - Set virtualenv path: `/home/yourusername/Student-Management-System/sms`

6. **Edit WSGI configuration file:**
   ```python
   import sys
   import os

   # Add your project directory to the sys.path
   project_home = '/home/yourusername/Student-Management-System'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path

   # Set environment variables
   os.environ['DB_HOST'] = 'yourusername.mysql.pythonanywhere-services.com'
   os.environ['DB_USER'] = 'yourusername'
   os.environ['DB_PASSWORD'] = 'your_db_password'
   os.environ['DB_NAME'] = 'yourusername$sms'

   # Import Flask app
   from app import app as application
   ```

7. **Update app.py for production:**
   ```python
   # Change debug mode
   if __name__ == "__main__":
       app.run(debug=False)  # Set to False in production
   ```

8. **Reload web app** - Click the green "Reload" button

Your app will be live at: `https://yourusername.pythonanywhere.com`

---

## Option 2: Render (Modern, Free Tier)

### Features:
- Automatic deployments from Git
- Free PostgreSQL/MySQL database
- HTTPS by default
- Easy environment variables

### Steps:

1. **Create account at [Render](https://render.com)**

2. **Create a Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose a name for your service

3. **Configure the service:**
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Add environment variables:**
     - `DB_HOST`
     - `DB_USER`
     - `DB_PASSWORD`
     - `DB_NAME`
     - `FLASK_ENV=production`

4. **Create a MySQL database:**
   - Click "New +" → "MySQL" (or use external MySQL)
   - Note the connection details

5. **Add `gunicorn` to requirements.txt:**
   ```
   gunicorn==21.2.0
   ```

6. **Update app.py:**
   ```python
   import os

   # Database configuration with environment variables
   con = mysql.connect(
       host=os.getenv('DB_HOST', 'localhost'),
       user=os.getenv('DB_USER', 'root'),
       password=os.getenv('DB_PASSWORD', '123456789'),
       database=os.getenv('DB_NAME', 'sms')
   )

   if __name__ == "__main__":
       port = int(os.getenv('PORT', 5000))
       app.run(host='0.0.0.0', port=port, debug=False)
   ```

7. **Deploy** - Push to GitHub and Render will auto-deploy

Your app will be live at: `https://your-app-name.onrender.com`

---

## Option 3: Railway (Fastest Setup)

### Features:
- One-click MySQL database
- Automatic HTTPS
- Environment variables
- Free tier available

### Steps:

1. **Create account at [Railway](https://railway.app)**

2. **Deploy from GitHub:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add MySQL database:**
   - Click "+ New" → "Database" → "MySQL"
   - Railway will automatically set connection variables

4. **Add environment variables:**
   - Go to your service → "Variables"
   - Add `FLASK_ENV=production`

5. **Create `Procfile`:**
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. **Update requirements.txt** to include `gunicorn`

7. **Railway will auto-deploy** on every git push

---

## Option 4: Traditional VPS (DigitalOcean, AWS, Linode)

### For production-grade deployments

### Requirements:
- Ubuntu 20.04+ server
- Root/sudo access
- Domain name (optional)

### Steps:

1. **Install required packages:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx mysql-server
   ```

2. **Clone repository:**
   ```bash
   cd /var/www
   git clone https://github.com/yourusername/Student-Management-System.git
   cd Student-Management-System
   ```

3. **Set up virtual environment:**
   ```bash
   python3 -m venv sms
   source sms/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Configure MySQL:**
   ```bash
   sudo mysql_secure_installation
   sudo mysql
   ```
   ```sql
   CREATE DATABASE sms;
   CREATE USER 'smsuser'@'localhost' IDENTIFIED BY 'strong_password';
   GRANT ALL PRIVILEGES ON sms.* TO 'smsuser'@'localhost';
   FLUSH PRIVILEGES;
   EXIT;
   ```
   ```bash
   mysql -u smsuser -p sms < sms_data.sql
   ```

5. **Create systemd service** `/etc/systemd/system/sms.service`:
   ```ini
   [Unit]
   Description=Student Management System
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/Student-Management-System
   Environment="PATH=/var/www/Student-Management-System/sms/bin"
   Environment="DB_HOST=localhost"
   Environment="DB_USER=smsuser"
   Environment="DB_PASSWORD=strong_password"
   Environment="DB_NAME=sms"
   ExecStart=/var/www/Student-Management-System/sms/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 app:app

   [Install]
   WantedBy=multi-user.target
   ```

6. **Configure Nginx** `/etc/nginx/sites-available/sms`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }

       location /static {
           alias /var/www/Student-Management-System/static;
       }
   }
   ```

7. **Enable and start services:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/sms /etc/nginx/sites-enabled
   sudo systemctl start sms
   sudo systemctl enable sms
   sudo systemctl restart nginx
   ```

8. **Set up SSL with Let's Encrypt:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

---

## Pre-Deployment Checklist

### Security:
- [ ] Change `app.secret_key` to a strong random value
- [ ] Set `debug=False` in production
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Update CORS settings if needed
- [ ] Set secure session cookie settings

### Database:
- [ ] Create production database
- [ ] Import schema and initial data
- [ ] Set up database backups
- [ ] Use strong database passwords

### Code Updates:
- [ ] Add environment variable support
- [ ] Install `gunicorn` for production server
- [ ] Update allowed hosts/CORS
- [ ] Set up logging

### Required Files:

**requirements.txt** (add gunicorn):
```
Flask==3.0.0
mysql-connector-python==8.2.0
Werkzeug==3.0.1
gunicorn==21.2.0
```

**Create `.env` file** (don't commit this!):
```
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=sms
FLASK_SECRET_KEY=your-super-secret-key-here
FLASK_ENV=production
```

**Update app.py** to use environment variables:
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key')

con = mysql.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    user=os.getenv('DB_USER', 'root'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME', 'sms')
)
```

**Add to requirements.txt:**
```
python-dotenv==1.0.0
```

---

## Comparison Table

| Platform | Difficulty | Free Tier | Database | Best For |
|----------|-----------|-----------|----------|----------|
| **PythonAnywhere** | ⭐ Easy | ✅ Yes | MySQL 200MB | Beginners, small projects |
| **Render** | ⭐⭐ Medium | ✅ Yes | MySQL/PostgreSQL | Modern apps, auto-deploy |
| **Railway** | ⭐⭐ Medium | ✅ Yes | MySQL included | Quick deployments |
| **VPS (DO/AWS)** | ⭐⭐⭐⭐ Hard | ❌ No | Self-managed | Production, full control |

---

## My Recommendation

**For your first deployment:** Start with **PythonAnywhere** or **Render**
- Easy to set up
- Free tier available
- Good for learning
- Can migrate later

**For production:** Use a **VPS with proper configuration**
- Full control
- Better performance
- Professional setup

---

## Common Issues & Solutions

### Issue: "Can't connect to database"
**Solution:** Check environment variables and database host/credentials

### Issue: "500 Internal Server Error"
**Solution:** Check logs, ensure debug=False, verify all dependencies installed

### Issue: "Static files not loading"
**Solution:** Configure static file serving in WSGI/Nginx

### Issue: "Session not persisting"
**Solution:** Set `app.secret_key` and ensure cookies are not blocked

---

## Need Help?

- Check deployment platform docs
- Review application logs
- Test locally with `gunicorn app:app` before deploying
- Use environment variables for all sensitive data

Good luck with your deployment! 🚀
