# Simple deployment instructions for various platforms

## Quick Deploy Commands

### For Vercel (Frontend):
```bash
cd frontend/
npx vercel --prod
```

### For Railway (Backend):
```bash
cd backend/
railway deploy
```

### For Netlify (Frontend):
```bash
cd frontend/
npm run build
# Then drag & drop the 'build' folder to Netlify
```

### For Render (Backend):
```bash
# Push backend/ folder to GitHub
# Connect to Render.com
# Build command: pip install -r requirements.txt
# Start command: python server.py
```

## Environment Variables Needed:

**Frontend (.env):**
```
REACT_APP_BACKEND_URL=https://your-backend-url.com
```

**Backend (.env):**
```
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/rbc_community
```

## Admin Access:
Password: `Rbcadminpass2025`