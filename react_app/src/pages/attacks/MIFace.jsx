// MIFace Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/attacks/MIFace.css";

let pageTitle = "MIFace";

function MIFace() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implementation of the MIFace algorithm from Fredrikson et al. (2015).
          While in that paper the attack is demonstrated specifically against
          face recognition models, it is applicable more broadly to classifiers
          with continuous features which expose class gradients.
        </p>
        <a className="details-link" href="https://dl.acm.org/doi/10.1145/2810103.2813677">
          See Details Here
        </a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default MIFace;
