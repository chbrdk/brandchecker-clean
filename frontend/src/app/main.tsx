import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.tsx';

// Import CSS tokens and global styles
import '../styles/tokens/index.css';
import '../index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
