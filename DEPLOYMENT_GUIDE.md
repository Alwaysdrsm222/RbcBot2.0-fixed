# 🐅 RBC Community Website - Deployment Guide

## 📦 What's Included
This package contains your complete RBC Community website with tiger theme:
- **Frontend**: React app with animations and tiger theme
- **Backend**: FastAPI server with MongoDB integration
- **Admin Panel**: Password-protected giveaway management
- **Database**: MongoDB setup for giveaway persistence

## 🌟 Features
- ✅ Beautiful tiger-themed design with orange/yellow animations
- ✅ Real-time giveaway system with countdown timers
- ✅ Admin panel (password: `Rbcadminpass2025`)
- ✅ Discord integration (https://discord.gg/letsgo)
- ✅ Community stats and features
- ✅ Mobile-responsive design

## 🚀 Recommended FREE Deployment Platforms

### 🥇 Option 1: Vercel (Frontend) + Railway (Backend) [RECOMMENDED]

**Frontend on Vercel:**
1. Go to [vercel.com](https://vercel.com) and sign up
2. Connect your GitHub account
3. Upload the `frontend/` folder to a new GitHub repo
4. Import project in Vercel
5. Set environment variable: `REACT_APP_BACKEND_URL=your-railway-backend-url`
6. Deploy!

**Backend on Railway:**
1. Go to [railway.app](https://railway.app) and sign up
2. Create new project → Deploy from GitHub
3. Upload the `backend/` folder to GitHub
4. Add MongoDB addon in Railway
5. Set environment variable: `MONGO_URL=your-mongodb-connection-string`
6. Deploy!

### 🥈 Option 2: Netlify (Frontend) + Render (Backend)

**Frontend on Netlify:**
1. Go to [netlify.com](https://netlify.com)
2. Drag & drop the `frontend/` folder
3. Set build command: `npm run build`
4. Set environment variable: `REACT_APP_BACKEND_URL=your-render-backend-url`

**Backend on Render:**
1. Go to [render.com](https://render.com)
2. Create new Web Service from GitHub
3. Upload `backend/` folder
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python server.py`
6. Add MongoDB connection string

### 🥉 Option 3: GitHub Pages (Frontend) + Heroku (Backend)

**Frontend on GitHub Pages:**
1. Upload `frontend/` to GitHub repo
2. Enable GitHub Pages in repository settings
3. Set environment variable in build process

**Backend on Heroku:**
1. Install Heroku CLI
2. Upload `backend/` folder
3. Create Procfile: `web: python server.py`
4. Add MongoDB Atlas addon

## 🛠️ Manual Deployment Steps

### Prerequisites
- Node.js 16+ and npm/yarn
- Python 3.8+
- MongoDB database (local or cloud)

### 1. Frontend Setup
```bash
cd frontend/
npm install
# or yarn install

# Set your backend URL
echo "REACT_APP_BACKEND_URL=http://your-backend-url" > .env

# Build for production
npm run build
# or yarn build
```

### 2. Backend Setup
```bash
cd backend/
pip install -r requirements.txt

# Set your MongoDB URL
echo "MONGO_URL=mongodb://your-mongodb-url" > .env

# Run the server
python server.py
```

### 3. Database Setup
- **MongoDB Atlas (Free)**: Sign up at [mongodb.com/atlas](https://mongodb.com/atlas)
- **Local MongoDB**: Install MongoDB locally
- The app will automatically create the `rbc_community` database and `giveaways` collection

## 🔧 Configuration Files

### Frontend (.env)
```
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

### Backend (.env)
```
MONGO_URL=mongodb://your-mongodb-connection-string
```

## 🔐 Admin Access
- **Admin Password**: `Rbcadminpass2025`
- **Admin Panel**: Click "Admin Panel" button on the website
- **Features**: Add, edit, delete giveaways

## 🎯 Testing Your Deployment

1. **Frontend**: Visit your deployed URL
2. **Backend**: Check `your-backend-url/api/health`
3. **Database**: Create a test giveaway in admin panel
4. **Discord Link**: Verify https://discord.gg/letsgo works

## 📱 Features to Test

- ✅ Tiger animations and responsive design
- ✅ Discord link functionality  
- ✅ Giveaway countdown timers
- ✅ Admin panel login and giveaway management
- ✅ Real-time giveaway updates (auto-refresh every 30s)

## 🆘 Troubleshooting

**Common Issues:**

1. **CORS Errors**: Make sure your backend URL is correctly set in frontend .env
2. **Database Connection**: Verify MongoDB URL is correct
3. **Admin Login**: Password is case-sensitive: `Rbcadminpass2025`
4. **Images Not Loading**: Check internet connection for Pexels/Unsplash images

**Environment Variables:**
- Frontend needs `REACT_APP_BACKEND_URL`
- Backend needs `MONGO_URL`
- Both must be set before deployment

## 🎉 You're Ready!

Your RBC Community website is ready to roar! 🐅

- **Discord Community**: https://discord.gg/letsgo
- **Admin Panel**: Use password `Rbcadminpass2025`
- **Tiger Theme**: Orange/yellow animations throughout
- **Giveaway System**: Real-time updates and countdown timers

**Need Help?** 
- Check platform documentation
- Verify environment variables
- Test API endpoints individually

Good luck with your community website! 🚀🐅