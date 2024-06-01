import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/attacks/FirstGradientMethod.css";

let pageTitle = "First Gradient Method";

function FirstGradientMethod() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          This attack was originally implemented by Goodfellow et al. (2015)
          with the infinity norm (and is known as the “Fast Gradient Sign
          Method”). This implementation extends the attack to other norms, and
          is therefore called the Fast Gradient Method.
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1412.6572">
          See Details Here
        </a>
        <hr/>
      </div>
      <Footer />
    </div>
  );
}

export default FirstGradientMethod;
