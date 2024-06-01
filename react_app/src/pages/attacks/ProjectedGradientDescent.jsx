// Projected Gradient Descent Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/attacks/ProjectedGradientDescent.css";

let pageTitle = "Projected Gradient Descent";

function ProjectedGradientDescent() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          The Projected Gradient Descent attack is an iterative method in which,
          after each iteration, the perturbation is projected on an lp-ball of
          specified radius (in addition to clipping the values of the
          adversarial sample so that it lies in the permitted data range). This
          is the attack proposed by Madry et al. for adversarial training.
        </p>
        <a className="details-link" href="https://arxiv.org/abs/1706.06083">
          See Details Here
        </a>
        <hr/>
      </div>
      <Footer />
    </div>
  );
}

export default ProjectedGradientDescent;
