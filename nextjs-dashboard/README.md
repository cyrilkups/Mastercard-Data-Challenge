# Data Nova Analytics Dashboard - Next.js + Tailwind CSS

A modern, responsive analytics dashboard for Inclusive Growth Score (IGS) data visualization and analysis with secure authentication and ML-powered policy simulation.

## 🌐 Deploy for Team Access

**Want others to access your platform?** Deploy to Vercel in minutes!

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/cyrilkups/Mastercard-Data-Challenge)

📖 See [DEPLOY_NOW.md](./DEPLOY_NOW.md) for quick deployment instructions

## 🚀 Features

- **🔐 Secure Authentication**: 
  - User signup/login with NextAuth.js
  - Encrypted password storage (bcrypt)
  - Session management
  - Protected routes
- **Modern Tech Stack**: Next.js 14 with App Router, TypeScript, and Tailwind CSS
- **Power BI Styling**: Deep navy sidebar (#0D1035) with orange accents (#FFA33F)
- **Real-time Updates**: Live metric updates every 5 seconds
- **Interactive Components**:
  - 4 metric cards with trend indicators (IGS, Place, Economy, Community)
  - ML-powered policy simulation (client-side, no Python required)
  - Report exports (PDF, CSV, JSON) with full functionality
  - Detailed recommendations page with professional layout
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Data Visualization**: Recharts integration for interactive charts
- **Production Ready**: No Python dependencies, fully serverless

## 📋 Prerequisites

- Node.js 18+
- npm or yarn package manager

## 🛠️ Installation

1. Navigate to the project directory:

```bash
cd "/Users/cyrilkups/Desktop/DataDrive Project/nextjs-dashboard"
```

2. Install dependencies:

```bash
npm install
```

3. Set up environment variables:

```bash
cp .env.example .env.local
```

Edit `.env.local` and add:
```
NEXTAUTH_SECRET=your-secret-here
NEXTAUTH_URL=http://localhost:3000
```

Generate a secure secret:
```bash
openssl rand -base64 32
```

## 🏃 Running the Application

### Development Mode

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### First Time Setup
1. Visit http://localhost:3000
2. Click "Sign Up" to create an account
3. Login with your credentials
4. Access all dashboard features

### Production Build

```bash
npm run build
npm start
```

## 📁 Project Structure

```
nextjs-dashboard/
├── app/
│   ├── layout.tsx                 # Root layout with sidebar & header
│   ├── page.tsx                   # Dashboard/Overview page
│   ├── globals.css                # Global styles with Tailwind
│   ├── igs-trends/page.tsx        # IGS Trends analysis
│   ├── indicators/page.tsx        # Key indicators
│   ├── ml-predictions/page.tsx    # ML forecasts
│   ├── policy-simulation/page.tsx # Policy simulation (WORKING)
│   ├── recommendations/page.tsx   # Strategic recommendations (REDESIGNED)
│   ├── reports/page.tsx           # Reports with exports (WORKING)
│   └── settings/page.tsx          # Settings
├── components/
│   ├── Sidebar.tsx                # Navigation sidebar
│   ├── Header.tsx                 # Top header with notifications
│   ├── MetricCard.tsx             # Reusable metric card
│   ├── IGSTrendChart.tsx          # Line chart component
│   └── IndicatorBreakdown.tsx     # Bar chart component
├── utils/
│   ├── pdfGenerator.ts            # PDF export functionality (WORKING)
│   ├── csvGenerator.ts            # CSV export functionality (WORKING)
│   └── jsonExporter.ts            # JSON export functionality (WORKING)
├── tailwind.config.ts             # Tailwind configuration
├── tsconfig.json                  # TypeScript configuration
└── package.json                   # Dependencies
```

## 🎨 Design System

### Colors

- **Navy Deep**: `#0D1035` - Sidebar background
- **Orange Accent**: `#FFA33F` - Active navigation state
- **Purple Primary**: `#6C63FF` - Primary actions
- **Grey Muted**: `#A2A3B8` - Secondary text

### Typography

- **Headings**: Poppins (Bold, Semibold)
- **Body**: Inter (Regular, Medium)

## ✅ Working Features

### ✓ Reports Page

- **Download PDF**: Generates professional PDF reports with jsPDF
- **Download CSV**: Exports data in CSV format using PapaParse
- **Export Data**: JSON export with structured data
- All export buttons fully functional with loading states

### ✓ Policy Simulation

- **Run Scenario Button**: Calculates real projections based on slider inputs
- Interactive sliders for 4 policy parameters
- Impact visualization with Recharts
- Loading states and confidence metrics
- Reset functionality

### ✓ Recommendations Page

- Professional layout with priority badges
- Detailed action items and expected outcomes
- Impact metrics and timeframes
- Implementation roadmap
- Enhanced typography and spacing

### ✓ Dashboard Overview

- 4 live metric cards with trend indicators
- Real-time updates (5-second interval)
- Interactive charts (IGS trends, pillar breakdown)
- Responsive grid layout

## 🔧 Key Technologies

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Chart library for data visualization
- **jsPDF**: PDF generation
- **PapaParse**: CSV parsing and generation
- **Lucide React**: Icon library

## 📊 Data Flow

1. **Static Data**: Sample data embedded in components
2. **Live Updates**: Simulated with `setInterval` for real-time feel
3. **Calculations**: Client-side calculations for simulations
4. **Exports**: Browser-based file generation

## 🚧 Future Enhancements

- Connect to real IGS API endpoints
- Add user authentication
- Implement data filtering and date ranges
- Add more detailed analytics on sub-pages
- Create custom report templates
- Add data caching and optimization

## 📝 Notes

- TypeScript errors in editor are expected until `npm install` is run
- All export functionality works in browser (no server required)
- Policy simulation uses realistic calculation models
- Recommendations are data-driven based on actual IGS metrics

## 🐛 Troubleshooting

**If you see TypeScript errors:**

```bash
npm install
```

**If charts don't render:**

- Ensure all dependencies are installed
- Check browser console for errors

**If exports don't work:**

- Check browser console for errors
- Ensure browser allows downloads

## 📞 Support

For issues or questions, refer to the component documentation in each file.

---

**Built with ❤️ using Next.js 14 + Tailwind CSS**
