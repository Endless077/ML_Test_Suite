// Total Variance Minimization Page
import React from "react";
import Navbar from "../../components/header";
import Footer from "../../components/footer";

import "../../styles/defenses/TotalVarMin.css";

let pageTitle = "Total Variance Minimization";

function TotalVarMin() {
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <p className="description">
          Implement the total variance minimization defence approach. Please
          keep in mind the limitations of defences. For more information on the
          limitations of this defence, see{" "}
          <a href="https://arxiv.org/abs/1802.00420">this article</a>. For
          details on how to evaluate classifier security in general, see{" "}
          <a href="https://arxiv.org/abs/1902.06705">this article</a>.
        </p>
        <a href="https://openreview.net/forum?id=SyJ7ClWCb">See Details Here</a>
        <hr />
      </div>
      <Footer />
    </div>
  );
}

export default TotalVarMin;
