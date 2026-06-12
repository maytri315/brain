# Vercel Deployment

This frontend is ready to deploy on Vercel.

## Required setup

1. Push the repository to GitHub.
2. Import the repo into Vercel.
3. Set the project root directory to `prot-refine-ai/frontend`.
4. Add this environment variable in Vercel:

```bash
VITE_API_BASE_URL=https://your-backend-domain.com
```

5. Leave the build command as `npm run build`.
6. Leave the output directory as `dist`.

## Important note

Vercel will host only the React frontend. The FastAPI backend must be deployed separately on Render, Railway, or another Python host, and the frontend must point to that backend URL through `VITE_API_BASE_URL`.

## Local preview

```bash
npm install
npm run build
npm run preview
```
