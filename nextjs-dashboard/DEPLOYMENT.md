# Deployment Guide - Data Nova Platform

## Deploy to Vercel (Recommended)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
cd nextjs-dashboard
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? **Your account**
- Link to existing project? **No**
- Project name? **data-nova** (or your preferred name)
- Directory? **./nextjs-dashboard**
- Override settings? **No**

### Step 4: Set Environment Variables

After deployment, you need to set the environment variables in Vercel:

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add these variables:

```
NEXTAUTH_SECRET=<generate-a-secret-key>
NEXTAUTH_URL=https://your-app.vercel.app
```

To generate a secure secret:
```bash
openssl rand -base64 32
```

### Step 5: Redeploy
After adding environment variables:
```bash
vercel --prod
```

## Alternative: Deploy to Netlify

### Step 1: Install Netlify CLI
```bash
npm install -g netlify-cli
```

### Step 2: Login and Deploy
```bash
cd nextjs-dashboard
netlify login
netlify init
netlify deploy --prod
```

### Step 3: Set Environment Variables
In Netlify dashboard:
- Go to **Site settings** → **Environment variables**
- Add `NEXTAUTH_SECRET` and `NEXTAUTH_URL`

## Important Notes

### User Data Persistence
The current setup uses file-based storage (`data/users.json`). For production, consider:

1. **Vercel KV** (Redis-compatible)
2. **MongoDB Atlas** (free tier available)
3. **Supabase** (PostgreSQL)
4. **PlanetScale** (MySQL)

### Security Checklist
- ✅ Change `NEXTAUTH_SECRET` to a strong random value
- ✅ Update `NEXTAUTH_URL` to your production domain
- ✅ Enable HTTPS (automatic with Vercel/Netlify)
- ✅ Review CORS settings if needed
- ✅ Set up monitoring and error tracking

### Testing Deployment
After deployment, test:
1. User signup works
2. User login works
3. Session persistence
4. All dashboard features
5. Export functionality (PDF, CSV, JSON)
6. Policy simulation

## Quick Deploy with Vercel Button

Add this to your README:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/cyrilkups/Mastercard-Data-Challenge/tree/main/nextjs-dashboard)

## Troubleshooting

### Issue: Authentication not working
- Check `NEXTAUTH_SECRET` is set
- Verify `NEXTAUTH_URL` matches your domain
- Ensure environment variables are deployed

### Issue: Users not persisting
- File-based storage doesn't work well on Vercel (read-only filesystem)
- Migrate to a database solution (see User Data Persistence above)

### Issue: API routes failing
- All API routes are now serverless-compatible (no Python dependencies)
- Check Vercel function logs for errors

## Post-Deployment

1. Share the URL: `https://your-app.vercel.app`
2. Users can signup/login securely
3. All features work over HTTPS
4. Data is encrypted in transit
