# AI Financial Coach - React Frontend

Modern, beautiful web interface for the AI Financial Coach application.

## 🎨 Design

Inspired by:
- **Stripe** - Clean, professional financial UI
- **Linear** - Modern gradients & animations  
- **Plaid** - Data visualization
- **Vercel** - Minimalist design

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build
```

## 🛠️ Tech Stack

- **React 18** + TypeScript
- **Vite** - Fast build tool
- **Tailwind CSS** - Styling
- **Framer Motion** - Animations
- **Recharts** - Charts
- **React Query** - Server state
- **React Router** - Navigation
- **Lucide Icons** - Icons

## 📁 Structure

```
src/
├── components/
│   ├── ui/              # Reusable UI components
│   ├── upload/          # File upload
│   ├── dashboard/       # Dashboard cards
│   └── charts/          # Visualizations
├── pages/
│   ├── Home.tsx         # Landing page
│   └── Analysis.tsx     # Results dashboard
├── lib/
│   ├── api.ts           # API client
│   └── utils.ts         # Utilities
└── App.tsx              # Root component
```

## 🎯 Features

### Home Page
- Gradient background
- Drag & drop file upload
- Upload progress animation
- Feature cards

### Analysis Dashboard
- Financial summary card
- 4 AI analysis cards:
  - 💳 Debt Analysis
  - 💰 Savings Strategy
  - 📊 Budget Optimizer
  - ⚠️ Risk Score
- Interactive charts
- Export PDF

## 🎨 Design System

### Colors
- Primary: Blue (#3b82f6)
- Success: Green (#10b981)
- Warning: Amber (#f59e0b)
- Danger: Red (#ef4444)

### Animations
- Card hover effects
- Number count-ups
- Progress bars
- Smooth transitions
- Loading states

## 🔧 Configuration

### Environment Variables

Create `.env` file:

```
VITE_API_URL=http://localhost:8000
```

### API Integration

The frontend connects to the FastAPI backend on port 8000.

Make sure the backend is running:
```bash
cd ../backend
uvicorn backend.main:app --reload
```

## 📱 Responsive

- Mobile: Single column
- Tablet: 2 columns
- Desktop: 2-3 columns

## 🚢 Deployment

### Build
```bash
npm run build
# Outputs to dist/
```

### Deploy to Vercel
```bash
vercel deploy
```

### Deploy to Netlify
```bash
netlify deploy --prod
```

## 🎉 Ready to Use!

The frontend is production-ready with:
- ✅ Beautiful UI
- ✅ Smooth animations
- ✅ Responsive design
- ✅ API integration
- ✅ Error handling
- ✅ TypeScript
