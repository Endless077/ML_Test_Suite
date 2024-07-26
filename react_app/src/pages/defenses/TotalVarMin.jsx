// TotalVarMin Page
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Navbar from "../../components/header";
import Footer from "../../components/footer";

import UploadSection from "../../components/uploadSection";
import TotalVarMinInput from "../../components/input/defenses/totalVarMinInput";

import "../../styles/defenses/TotalVarMin.css";
import Swal from "sweetalert2";

let pageTitle = "Total Variance Minimization";
import {
  showErrorAlert,
  uploadModel,
  uploadDataset,
  startDefenseProcess,
} from "../../utils/functions";

function TotalVarMin() {
  const [fileUploaded, setFileUploaded] = useState(false);
  const [datasetSelected, setDatasetSelected] = useState(false);
  const [showPersonalUpload, setShowPersonalUpload] = useState(false);

  const [model, setModel] = useState(null);
  const [dataset, setDataset] = useState(null);

  const navigate = useNavigate();

  /* *** */

  const [epochs, setEpochs] = useState(1);
  const [batchSize, setBatchSize] = useState(32);
  const [evasionAttack, setEvasionAttack] = useState("FGM");
  const [samplePercentage, setSamplePercentage] = useState(0.1);
  const [prob, setProb] = useState(0.3);
  const [norm, setNorm] = useState(2);
  const [lamb, setLamb] = useState(0.5);
  const [solver, setSolver] = useState("L-BFGS-B");
  const [maxIter, setMaxIter] = useState(10);

  const [epsValue, setEpsValue] = useState(0.3);
  const [epsStepValue, setEpsStepValue] = useState(0.1);
  const [normValue, setNormValue] = useState("inf");

  /* ******************************************************************************************* */

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    setFileUploaded(!!file);
    setModel(file);
  };

  const handleCheckboxChange = (event) => {
    if (fileUploaded) {
      const isPersonal = event.target.value === "personal";
      setShowPersonalUpload(isPersonal);
      setDatasetSelected(!isPersonal);
      setDataset(event.target.value);
    }
  };

  const handledatasetUpload = (event) => {
    const dataset = event.target.files[0];
    setDataset(dataset);
    setDatasetSelected(true);
  };

  /* ******************************************************************************************* */

  const handleEpochsChange = (event) => {
    const newValue = event.target.value;
    if (newValue === "" || (/^\d+$/.test(newValue) && parseInt(newValue) > 0)) {
      setEpochs(newValue);
    }
  };

  const handleBatchSizeChange = (event) => {
    const newValue = event.target.value;
    if (newValue === "" || (/^\d+$/.test(newValue) && parseInt(newValue) > 0)) {
      setBatchSize(newValue);
    }
  };

  const handleEvasionAttackChange = (event) => {
    setEvasionAttack(event.target.value);
  };

  const handleSamplePercentageChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setSamplePercentage(newValue);
    }
  };

  const handleProbChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setProb(newValue);
    }
  };

  const handleNormIntChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setNorm(newValue);
  };

  const handleLambChange = (event) => {
    let newValue = event.target.value;
    if (newValue === "" || newValue === "0") {
      newValue = "0.1";
    } else if (!isNaN(parseFloat(newValue))) {
      newValue = Math.max(0, parseFloat(newValue));
    }
    setLamb(newValue);
  };

  const handleSolverChange = (event) => {
    const newValue = event.target.value;
    setSolver(newValue);
  };

  const handleMaxIterChange = (event) => {
    const newValue = event.target.value;
    if (newValue === "" || (/^\d+$/.test(newValue) && parseInt(newValue) > 0)) {
      setMaxIter(newValue);
    }
  };

  /* ******************************************************************************************* */

  const handleEpsChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setEpsValue(newValue);
    }
  };

  const handleEpsStepChange = (event) => {
    const newValue = parseFloat(event.target.value);
    if (!isNaN(newValue) && newValue >= 0.1 && newValue <= 1) {
      setEpsStepValue(newValue);
    }
  };

  const handleNormChange = (event) => {
    const newValue = event.target.value;
    if (["inf", "1", "2"].includes(newValue)) {
      setNormValue(newValue);
    }
  };

  /* ******************************************************************************************* */

  const validateInputs = () => {
    const errors = [];

    if (!fileUploaded) {
      errors.push("Upload a model file.");
    }

    if (!datasetSelected) {
      errors.push("Select a dataset.");
    }

    if (isNaN(parseInt(epochs)) || parseInt(epochs) <= 0 || epochs === "") {
      errors.push("Enter a valid number of epochs (positive value).");
    }

    if (isNaN(parseInt(batchSize)) || parseInt(batchSize) <= 0) {
      errors.push("Enter a valid batch size (positive value).");
    }

    if (
      isNaN(parseFloat(samplePercentage)) ||
      samplePercentage < 0.1 ||
      samplePercentage > 1
    ) {
      errors.push("Enter a valid sample percentage (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(prob)) || prob < 0.1 || prob > 1) {
      errors.push("Enter a valid probability (between 0.1 and 1).");
    }

    if (isNaN(parseFloat(norm)) || parseFloat(norm) <= 0) {
      errors.push("Enter a valid norm interval (positive value).");
    }

    if (isNaN(parseFloat(lamb)) || parseFloat(lamb) <= 0) {
      errors.push("Enter a valid lambda value (positive value).");
    }

    if (isNaN(parseInt(maxIter)) || parseInt(maxIter) <= 0) {
      errors.push("Enter a valid max iterations value (positive value).");
    }

    if (isNaN(parseFloat(epsValue)) || epsValue < 0.1 || epsValue > 1) {
      errors.push("Enter a valid epsilon value (between 0.1 and 1).");
    }

    if (
      isNaN(parseFloat(epsStepValue)) ||
      epsStepValue < 0.1 ||
      epsStepValue > 1
    ) {
      errors.push("Enter a valid epsilon step value (between 0.1 and 1).");
    }

    return errors;
  };

  const uploadFiles = async () => {
    const uploadModelFetch = async () => {
      try {
        const filename = model.name.split(".").slice(0, -1).join(".");
        const uploadResponse = await uploadModel(filename, model);

        if (!uploadResponse.ok) {
          throw new Error(
            uploadResponse.detail ||
              "Error during model upload. Please try again later."
          );
        }

        const response = await uploadResponse.json();
        console.log(response);
        return true;
      } catch (error) {
        console.error("Error during model upload:", error);
        Swal.fire({
          icon: "error",
          title: "Error during model upload",
          text: error.message,
        });
        return false;
      }
    };

    const uploadDatasetFetch = async () => {
      try {
        const filename = dataset.name.split(".").slice(0, -1).join(".");
        const uploadResponse = await uploadDataset(filename, dataset);

        if (!uploadResponse.ok) {
          throw new Error(
            uploadResponse.detail ||
              "Error during dataset upload. Please try again later."
          );
        }

        const response = await uploadResponse.json();
        console.log(response);
        return true;
      } catch (error) {
        console.error("Error during dataset upload:", error);
        Swal.fire({
          icon: "error",
          title: "Error during dataset upload",
          text: error.message,
        });
        return false;
      }
    };

    const uploadModelCheck = await uploadModelFetch();
    return uploadModelCheck && showPersonalUpload
      ? await uploadDatasetFetch()
      : uploadModelCheck;
  };

  const handleLaunchClick = async () => {
    const errors = validateInputs();

    if (errors.length > 0) {
      showErrorAlert(errors);
      return;
    }

    const upload = await uploadFiles();
    if (upload) {
      const defenseModel = {
        epochs: epochs,
        batch_size: batchSize,
        filename: model.name.split(".").slice(0, -1).join("."),
        dataset_type: dataset,
        dataset_name: dataset.split(".").slice(0, -1).join(".") || dataset,
        evasion_attack: evasionAttack,
        samples_percentage: samplePercentage,
        eps: epsValue,
        eps_step: epsStepValue,
        norm: normValue,
        prob: prob,
        norm_value: norm,
        lamb_value: lamb,
        solver: solver,
        max_iter: maxIter,
      };

      console.log(attackModel);
      await startDefenseProcess(
        "preprocessor",
        "totalvarmin",
        defenseModel,
        navigate
      );
    }
  };

  /* ******************************************************************************************* */
  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content container mt-3">
        {/* First Section */}
        <p className="description">
          Implement the total variance minimization defence approach. Please
          keep in mind the limitations of defences. For more information on the
          limitations of this defence, see{" "}
          <a href="https://arxiv.org/abs/1802.00420">this article</a>. For
          details on how to evaluate classifier security in general, see{" "}
          <a href="https://arxiv.org/abs/1902.06705">this article</a>.
        </p>
        <a href="https://openreview.net/forum?id=SyJ7ClWCb">See Details Here</a>
        {/* Horizontal Divider */}
        <hr />
        {/* Upload Section */}
        <div className="row">
          <div className="col-md-5">
            <UploadSection
              action={pageTitle}
              fileUploaded={fileUploaded}
              showPersonalUpload={showPersonalUpload}
              handleFileUpload={handleFileUpload}
              handleCheckboxChange={handleCheckboxChange}
              handledatasetUpload={handledatasetUpload}
            />
          </div>
          {/* Vertical Divider */}
          <div className="col-md-2 d-flex align-items-center justify-content-center">
            <div className="vr custom-vr"></div>
          </div>
          {/* Input Section */}
          <div className="col-md-5">
            <TotalVarMinInput
              epochs={epochs}
              handleEpochsChange={handleEpochsChange}
              batchSize={batchSize}
              handleBatchSizeChange={handleBatchSizeChange}
              evasionAttack={evasionAttack}
              handleEvasionAttackChange={handleEvasionAttackChange}
              samplePercentage={samplePercentage}
              handleSamplePercentageChange={handleSamplePercentageChange}
              prob={prob}
              handleProbChange={handleProbChange}
              norm={norm}
              handleNormIntChange={handleNormIntChange}
              lamb={lamb}
              handleLambChange={handleLambChange}
              solver={solver}
              handleSolverChange={handleSolverChange}
              maxIter={maxIter}
              handleMaxIterChange={handleMaxIterChange}
              epsValue={epsValue}
              handleEpsChange={handleEpsChange}
              epsStepValue={epsStepValue}
              handleEpsStepChange={handleEpsStepChange}
              normValue={normValue}
              handleNormChange={handleNormChange}
              datasetSelected={datasetSelected}
            />
            {/* Launch Button */}
            <div className="launch-button-section text-end">
              <button
                className="btn btn-primary"
                disabled={!datasetSelected}
                onClick={handleLaunchClick}
              >
                Launch
              </button>
            </div>
          </div>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default TotalVarMin;
