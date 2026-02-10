# Quick Guide: Deploy to Render.com

## ✅ Prerequisites
- [x] Code pushed to GitHub: https://github.com/Mohith141012/Student_Management_System
- [ ] Render account created
- [ ] MySQL database ready

---

## 🚀 Deployment Steps

### 1️⃣ Create Account
- Go to [render.com](https://render.com)
- Sign up with GitHub
- Authorize Render

### 2️⃣ Create MySQL Database
1. Click **New +** → **MySQL**
2. Configure:
   - Name: `sms-database`
   - Database: `sms`
   - User: `smsuser`
   - Instance: **Free** or **Starter**
3. Click **Create Database**
4. **Save connection details** from the Info tab

### 3️⃣ Import Schema
```bash
# From your local machine, connect to Render database
mysql -h [HOSTNAME] -P 3306 -u [USERNAME] -p[PASSWORD] sms < sms_data.sql
```
Replace [HOSTNAME], [USERNAME], [PASSWORD] with values from Step 2.

### 4️⃣ Create Web Service
1. Click **New +** → **Web Service**
2. Connect your GitHub repository: `Student_Management_System`
3. Configure:

| Field | Value |
|-------|-------|
| Name | `student-management-system` |
| Region | Same as database |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |
| Instance Type | **Free** |

### 5️⃣ Set Environment Variables

Click **Add Environment Variable** and add:

```env
DB_HOST=<your-render-mysql-hostname>
DB_USER=smsuser
DB_PASSWORD=<your-mysql-password>
DB_NAME=sms
FLASK_SECRET_KEY=<generate-random-key>
FLASK_ENV=production
PORT=10000
```

**Generate FLASK_SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 6️⃣ Deploy
1. Click **Create Web Service**
2. Wait 2-5 minutes for deployment
3. Look for "✓ Your service is live 🎉"

### 7️⃣ Access Your App
Your app will be live at:
```
https://student-management-system-xxxx.onrender.com
```

---

## 🔍 Troubleshooting

### Issue: "Application Error" or 500 Error
**Solution:** Check the logs in Render dashboard
- Look for database connection errors
- Verify environment variables are set correctly
- Ensure database schema is imported

### Issue: "Can't connect to MySQL server"
**Solution:**
- Verify `DB_HOST` is the **Internal Hostname** (not external)
- Check database is in the same region as web service
- Ensure database password is correct (no spaces)

### Issue: "ModuleNotFoundError"
**Solution:**
- Check `requirements.txt` is in repository root
- Verify build command is: `pip install -r requirements.txt`
- Check build logs for errors

### Issue: Free tier sleeps after inactivity
**Solution:**
- Free tier services spin down after 15 mins of inactivity
- First request after sleep takes ~30 seconds
- Upgrade to Starter ($7/mo) for always-on

---

## 📊 Database Management

### View Database (MySQL Workbench)
1. Download MySQL Workbench
2. Create connection with Render credentials
3. Browse tables and data

### Backup Database
```bash
mysqldump -h [HOSTNAME] -P 3306 -u [USERNAME] -p[PASSWORD] sms > backup.sql
```

### Update Schema
```bash
mysql -h [HOSTNAME] -P 3306 -u [USERNAME] -p[PASSWORD] sms < updated_schema.sql
```

---

## 🔄 Auto-Deploy from GitHub

Render automatically deploys when you push to GitHub:

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push origin main

# Render will automatically deploy! 🎉
```

Watch deployment progress in Render dashboard → Your Service → Events

---

## 💰 Pricing

| Service | Free Tier | Paid |
|---------|-----------|------|
| **Web Service** | Yes (750 hrs/mo) | $7/mo (always on) |
| **MySQL Database** | No | $7/mo (Starter) |

**Note:** Free web services spin down after 15 mins of inactivity.

---

## 📝 Environment Variables Reference

| Variable | Example | Required | Description |
|----------|---------|----------|-------------|
| `DB_HOST` | `dpg-abc.oregon-postgres.render.com` | ✅ Yes | MySQL hostname from Render |
| `DB_USER` | `smsuser` | ✅ Yes | Database username |
| `DB_PASSWORD` | `SecurePass123!` | ✅ Yes | Database password |
| `DB_NAME` | `sms` | ✅ Yes | Database name |
| `FLASK_SECRET_KEY` | `a1b2c3d4...` | ✅ Yes | Random secret (32+ chars) |
| `FLASK_ENV` | `production` | ✅ Yes | Environment mode |
| `PORT` | `10000` | ✅ Yes | Render port (default) |

---

## ✅ Post-Deployment Checklist

- [ ] App loads successfully
- [ ] Can access home page
- [ ] Sign up works
- [ ] Login works
- [ ] Dashboard accessible
- [ ] Database queries work
- [ ] Admin features work
- [ ] Static files (CSS/JS) load

---

## 🔗 Useful Links

- [Your GitHub Repo](https://github.com/Mohith141012/Student_Management_System)
- [Render Dashboard](https://dashboard.render.com/)
- [Render Docs](https://render.com/docs)
- [Gunicorn Docs](https://docs.gunicorn.org/)

---

## 🆘 Need Help?

1. Check Render logs: Dashboard → Your Service → Logs
2. Review environment variables
3. Test database connection
4. Check GitHub repository is up to date

**Common fixes:**
```bash
# Test locally with production settings
export FLASK_ENV=production
gunicorn app:app

# Check if all dependencies install
pip install -r requirements.txt

# Verify database connection
python -c "import mysql.connector; print('MySQL connector working!')"
```

---

Good luck with your deployment! 🚀
