const express = require('express');
const path = require('path');
const app = express();
const port = process.env.PORT || 3000;

// Serve static files from the .next/static directory
app.use('/_next/static', express.static(path.join(__dirname, '.next/static')));

// Serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// Serve the Next.js app
app.get('*', (req, res) => {
  // For API requests, proxy to the backend
  if (req.path.startsWith('/api/')) {
    res.status(404).send('API endpoints are handled by the backend server');
    return;
  }
  
  // For all other requests, serve the Next.js app
  res.sendFile(path.join(__dirname, '.next/server/pages', req.path === '/' ? '/index.html' : `${req.path}.html`));
});

app.listen(port, () => {
  console.log(`Frontend server running on port ${port}`);
});
