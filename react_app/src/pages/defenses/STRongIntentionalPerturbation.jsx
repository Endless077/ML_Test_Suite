// STRong Intentional Perturbation Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/defenses/STRongIntentionalPerturbation.css";

let pageTitle = "STRong Intentional Perturbation";

function STRongIntentionalPerturbation() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implementation of STRIP: A Defence Against Trojan Attacks on Deep
          Neural Networks (Gao et. al. 2020)
        </p>
        <a href="https://arxiv.org/abs/1902.06531">See Details Here</a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default STRongIntentionalPerturbation;
