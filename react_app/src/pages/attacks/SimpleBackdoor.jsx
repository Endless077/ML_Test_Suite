// Simple Backdoor Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/attacks/SimpleBackdoor.css";

let pageTitle = "Simple Backdoor";

function SimpleBackdoor() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implementation of backdoor attacks introduced in Gu et al., 2017.
          Applies a number of backdoor perturbation functions and switches label
          to target label.
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1708.06733">
          See Details Here
        </a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default SimpleBackdoor;
