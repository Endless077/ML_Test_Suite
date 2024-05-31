// Activation Defense Page
import React from 'react';
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import '../../styles/defenses/AdversarialTrainer.css';

let pageTitle = "Activation Defense";

function ActivationDefense() {
    return (
        <div id='root'>
          <Navbar pageTitle={pageTitle}/>
          <div className="page-content">
          <h1>PlaceHolder</h1>
          </div>
          <Footer/>
        </div>
    );
}

export default ActivationDefense