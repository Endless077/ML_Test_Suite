import React from "react";
import PropTypes from "prop-types";

const UploadSection = ({
  action,
  fileUploaded,
  showPersonalUpload,
  handleFileUpload,
  handleCheckboxChange,
  handledatasetUpload,
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
        Upload here your model that you want to test for the {action}{" "}
        attack.
      </div>
      <div className="mb-3">
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
                <strong>Upload your personal dataset zip file</strong>
              </label>
              <input
                type="file"
                className="form-control"
                id="personalDatasetUpload"
                accept=".zip"
                multiple={false}
                onChange={handledatasetUpload}
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
  handledatasetUpload: PropTypes.func.isRequired,
  handleCheckboxChange: PropTypes.func.isRequired,
  action: PropTypes.string.isRequired,
  fileUploaded: PropTypes.bool.isRequired,
  showPersonalUpload: PropTypes.bool.isRequired,
};

export default UploadSection;
