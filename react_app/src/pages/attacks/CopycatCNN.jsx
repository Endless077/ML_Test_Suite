// CopycatCNN Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/attacks/CopycatCNN.css";

let pageTitle = "CopycatCNN";

function CopycatCNN() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implementation of the Copycat CNN attack from Rodrigues Correia-Silva
          et al. (2018).
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1806.05476">
          See Details Here
        </a>
        <hr/>
      </div>
      <Footer />
    </div>
  );
}

export default CopycatCNN;
