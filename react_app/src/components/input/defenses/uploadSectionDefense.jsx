import React from "react";
import PropTypes from 'prop-types';

const UploadSectionDefence = ({
  vulnerableFileUploaded,
  handleFileUploadVulnerable,
  robustFileUploaded,
  handleFileUploadModelRobust,
  alreadyCompiled,
  handleAlreadyCompiledChange,
  handleCheckboxChange,
  showPersonalUpload,
  attackName

}) => {
  const bothFilesUploaded = vulnerableFileUploaded && robustFileUploaded;

  return (
    <div>
      <div className="upload-section mb-4">
        <label htmlFor="vulnerableFileUpload" className="form-label">
          <strong>Upload your vulnerable model</strong>
        </label>
        <input
          type="file"
          className="form-control"
          id="vulnerableFileUpload"
          //accept=".h5,application/octet-stream"
          onChange={handleFileUploadVulnerable}
        />
      </div>
      <div className="upload-section mb-4">
        <label htmlFor="robustFileUpload" className="form-label">
          <strong>Upload your robust model</strong>
        </label>
        <input
          type="file"
          className="form-control"
          id="robustFileUpload"
          //accept=".h5,application/octet-stream"
          onChange={handleFileUploadModelRobust}
        />
      </div>
      <div className="description mb-4" style={{ fontSize: "14px" }}>
        Upload here your vulnerable and robust models that you want to test for the {attackName} attack.
      </div>
      <div className="mb-3">
        <div className="form-check">
          <input
            className="form-check-input"
            type="checkbox"
            value=""
            id="alreadyCompiledCheckbox"
            checked={alreadyCompiled}
            disabled={!bothFilesUploaded}
            onChange={handleAlreadyCompiledChange}
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
            checked
            disabled
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
            disabled={!bothFilesUploaded}
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
            disabled={!bothFilesUploaded}
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
            disabled={!bothFilesUploaded}
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
            disabled={!bothFilesUploaded}
          />
          <label className="form-check-label" htmlFor="personal">
            Personal
          </label>
        </div>
        {showPersonalUpload && (
          <div className="mt-3">
            <label htmlFor="personalFileUpload" className="form-label">
              Select your dataset directory
            </label>
            <input
              type="file"
              className="form-control"
              id="personalFileUpload"
              webkitdirectory="true"
              directory="true"
            />
          </div>
        )}
      </div>
    </div>
  );
};

UploadSectionDefence.propTypes = {
  handleFileUploadVulnerable: PropTypes.func.isRequired,
  handleFileUploadModelRobust: PropTypes.func.isRequired,
  handleCheckboxChange: PropTypes.func.isRequired,
  handleIsCompiledChange: PropTypes.func.isRequired,
  vulnerableFileUploaded: PropTypes.bool.isRequired,
  robustFileUploaded: PropTypes.bool.isRequired,
  isCompiled: PropTypes.bool.isRequired,
  attackName: PropTypes.string.isRequired,
  showPersonalUpload: PropTypes.bool.isRequired,
};

export default UploadSectionDefence;
