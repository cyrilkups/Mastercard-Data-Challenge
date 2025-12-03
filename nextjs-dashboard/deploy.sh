#!/bin/bash

# Deployment script for Data Nova Platform

echo "🚀 Data Nova Platform Deployment Script"
echo "========================================"
echo ""

# Check if vercel is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Navigate to dashboard directory
cd "$(dirname "$0")"

echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔐 Generating secure NEXTAUTH_SECRET..."
SECRET=$(openssl rand -base64 32)
echo "Generated secret: $SECRET"
echo ""

echo "📝 Creating .env.production file..."
cat > .env.production << EOF
NEXTAUTH_SECRET=$SECRET
NEXTAUTH_URL=https://your-app-name.vercel.app
EOF

echo "✅ .env.production created"
echo ""

echo "🌐 Deploying to Vercel..."
echo "Please update NEXTAUTH_URL in your Vercel dashboard after deployment"
echo ""

vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📌 Next steps:"
echo "1. Go to https://vercel.com/dashboard"
echo "2. Find your project"
echo "3. Go to Settings → Environment Variables"
echo "4. Update NEXTAUTH_URL to match your deployment URL"
echo "5. Redeploy if needed"
echo ""
echo "🎉 Your platform is now accessible to everyone!"
