// Adversarial Trainer Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/defenses/AdversarialTrainer.css";

let pageTitle = "Adversarial Trainer";

function AdversarialTrainer() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Class performing adversarial training based on a model architecture
          and one or multiple attack methods. Incorporates original adversarial
          training, ensemble adversarial training (
          <a href="https://arxiv.org/abs/1705.07204">article</a>), training on
          all adversarial data and other common setups. If multiple attacks are
          specified, they are rotated for each batch. If the specified attacks
          have as target a different model, then the attack is transferred. The
          ratio determines how many of the clean samples in each batch are
          replaced with their adversarial counterpart. Please keep in mind the
          limitations of defences. While adversarial training is widely regarded
          as a promising, principled approach to making classifiers more robust
          (see <a href="https://arxiv.org/abs/1802.00420">article</a>), very
          careful evaluations are required to assess its effectiveness case by
          case (see <a href="https://arxiv.org/abs/1902.06705">here</a>).
        </p>
        <a href="https://arxiv.org/abs/1705.07204">See Details Here</a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default AdversarialTrainer;
