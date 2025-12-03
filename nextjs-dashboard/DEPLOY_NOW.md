# 🚀 Quick Deployment Guide

## Deploy to Vercel in 3 Steps

### Option 1: One-Click Deploy (Fastest)

1. Click this button:
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/cyrilkups/Mastercard-Data-Challenge)

2. Set environment variables in Vercel:

   - `NEXTAUTH_SECRET` = (generate with: `openssl rand -base64 32`)
   - `NEXTAUTH_URL` = Your Vercel app URL (e.g., `https://your-app.vercel.app`)

3. Deploy!

### Option 2: Use Deploy Script

```bash
cd nextjs-dashboard
./deploy.sh
```

Then update `NEXTAUTH_URL` in Vercel dashboard with your actual deployment URL.

### Option 3: Manual Deployment

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
cd nextjs-dashboard
vercel --prod
```

## After Deployment

1. **Get your deployment URL** from Vercel (e.g., `https://data-nova-abc123.vercel.app`)

2. **Update environment variables** in Vercel dashboard:

   - Go to Settings → Environment Variables
   - Update `NEXTAUTH_URL` to your deployment URL
   - Redeploy if needed

3. **Share with your team!** Anyone can now:
   - Visit your app URL
   - Sign up for an account
   - Login securely
   - Access all features

## Features Available After Deployment

✅ **Secure Authentication**

- User signup with name, email, password
- Encrypted password storage (bcrypt)
- Session management
- Logout functionality

✅ **All Dashboard Features**

- IGS Trends visualization
- Policy simulation (ML-powered)
- Reports & Analytics
- PDF/CSV/JSON exports
- Feature importance charts

✅ **Production-Ready**

- HTTPS enabled automatically
- Serverless API routes
- No Python dependencies
- Fast global CDN
- Automatic scaling

## Troubleshooting

### Users can't login after deployment

- Check that `NEXTAUTH_URL` matches your deployment URL exactly
- Verify `NEXTAUTH_SECRET` is set in Vercel dashboard
- Clear browser cookies and try again

### Need help?

See full deployment guide: [DEPLOYMENT.md](./DEPLOYMENT.md)

## Security Notes

- All passwords are hashed with bcrypt
- HTTPS enforced automatically
- Session tokens are encrypted
- Environment variables are secure
- No sensitive data in git repository
