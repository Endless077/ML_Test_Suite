// CleanLabelBackdoor Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/attacks/CleanLabelBackdoor.css";

let pageTitle = "Clean Label Backdoor";

function CleanLabelBackdoor() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implementation of Clean-Label Backdoor Attack introduced in Turner et
          al., 2018. Applies a number of backdoor perturbation functions and
          does not change labels.
        </p>
        <a className="details-link" href="https://people.csail.mit.edu/madry/lab/cleanlabel.pdf">
          See Details Here
        </a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default CleanLabelBackdoor;
