import React from "react";
import PropTypes from "prop-types";

const UploadSection = ({
  handleFileUpload,
  handlePersonalDatasetUpload,
  handleAlreadyCompiled,
  handleCheckboxChange,
  attackName,
  fileUploaded,
  alreadyCompiled,
  showPersonalUpload,
}) => {
  return (
    <div>
      <div className="upload-section mb-4">
        <label htmlFor="modelUpload" className="form-label">
          <strong>Upload your model</strong>
        </label>
        <input
          type="file"
          className="form-control"
          id="modelUpload"
          accept=".h5,application/octet-stream"
          multiple={false}
          onChange={handleFileUpload}
        />
      </div>
      <div className="description mb-4" style={{ fontSize: "14px" }}>
        Upload here your model that you want to test for the {attackName}{" "}
        attack.
      </div>
      <div className="mb-3">
        <div className="form-check">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="alreadyCompiledCheckbox"
            checked={alreadyCompiled}
            disabled={!fileUploaded}
            onChange={handleAlreadyCompiled}
          />
          <label className="form-check-label" htmlFor="alreadyCompiledCheckbox">
            Already Compiled
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="defaultCheckbox"
            disabled
            checked
          />
          <label className="form-check-label" htmlFor="defaultCheckbox">
            Default (beta)
          </label>
        </div>
      </div>
      <div className="dataset-selection mt-4">
        <p>
          <strong>Select Dataset</strong>
        </p>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="mnist"
            value="mnist"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="mnist">
            Mnist
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="cifar10"
            value="cifar10"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="cifar10">
            Cifar 10
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="cifar100"
            value="cifar100"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="cifar100">
            Cifar 100
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="datasetOptions"
            id="personal"
            value="personal"
            onChange={handleCheckboxChange}
            disabled={!fileUploaded}
          />
          <label className="form-check-label" htmlFor="personal">
            Personal Dataset
          </label>
          {showPersonalUpload && (
            <div className="upload-section mt-2">
              <label htmlFor="personalDatasetUpload" className="form-label">
                <strong>Upload your personal dataset directory</strong>
              </label>
              <input
                type="file"
                className="form-control"
                id="personalDatasetUpload"
                accept=".zip"
                multiple={false}
                onChange={handlePersonalDatasetUpload}
              />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

UploadSection.propTypes = {
  handleFileUpload: PropTypes.func.isRequired,
  handlePersonalDatasetUpload: PropTypes.func.isRequired,
  handleAlreadyCompiled: PropTypes.func.isRequired,
  handleCheckboxChange: PropTypes.func.isRequired,
  attackName: PropTypes.string.isRequired,
  fileUploaded: PropTypes.bool.isRequired,
  alreadyCompiled: PropTypes.bool.isRequired,
  showPersonalUpload: PropTypes.bool.isRequired,
};

export default UploadSection;
