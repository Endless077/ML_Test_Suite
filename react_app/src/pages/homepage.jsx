import React from 'react';
import Navbar from "../components/header";
import Footer from "../components/footer";

function HomePage() {
  return (
    <div id="root">
      <Navbar />
      <div className="page-content">
        <h1>Insert Content</h1>
      </div>
      <Footer />
    </div>
  );
}

export default HomePage;
