// NotFound
import React from 'react';
import { Link } from 'react-router-dom';
import './styles/notFound.css';

const NotFound = () => {
  return (
    <div className="not-found-container">
      <img src="/assets/minimal_art_logo.png" alt="Page Not Found" className="not-found-logo" />
      <h1 className="not-found-title">Error 404</h1>
      <h2>Page Not Found</h2>
      <p className="not-found-subtitle">Are you lost?</p>
      <Link to="/" className="not-found-link">Back to Home</Link>
    </div>
  );
}

export default NotFound;
