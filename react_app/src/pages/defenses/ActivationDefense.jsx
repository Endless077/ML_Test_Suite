// Activation Defense Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/defenses/AdversarialTrainer.css";

let pageTitle = "Activation Defense";

function ActivationDefense() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Method from Chen et al., 2018 performing poisoning detection based on
          activations clustering. Please keep in mind the limitations of
          defences. For more information on the limitations of this defence, see{" "}
          <a href="https://arxiv.org/abs/1905.13409">this article</a> . For
          details on how to evaluate classifier security in general, see{" "}
          <a href="https://arxiv.org/abs/1902.06705">this article</a>.
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1811.03728">
          See Details Here
        </a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default ActivationDefense;
