import React from "react";
import PropTypes from "prop-types";

const AdversarialTrainerInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  evasionAttack,
  handleEvasionAttackChange,
  samplePercentage,
  handleSamplePercentageChange,
  ratio,
  handleRatioChange,
  epsValue,
  handleEpsChange,
  epsStepValue,
  handleEpsStepChange,
  normValue,
  handleNormChange,
  datasetSelected,
}) => {
  return (
    <div className="text-boxes-section mb-3">
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Epochs - The number of epochs</strong>
        </label>
        <input
          id="epochs"
          type="text"
          className="form-control"
          placeholder="epochs"
          value={epochs}
          onChange={handleEpochsChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Batch Size - The batch size for the attack</strong>
        </label>
        <input
          id="batch_size"
          type="text"
          className="form-control"
          placeholder="batch_size"
          value={batchSize}
          onChange={handleBatchSizeChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Evasion Attack - Type of evasion attack</strong>
        </label>
        <select
          className="form-select"
          value={evasionAttack}
          onChange={handleEvasionAttackChange}
          disabled={!datasetSelected}
        >
          <option value="fgm">FGM</option>
          <option value="pgd">PGD</option>
        </select>
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Sample Percentage - Percentage of samples used for attack
          </strong>
        </label>
        <input
          id="sample_percentage"
          type="number"
          step="0.01"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="sample_percentage"
          value={samplePercentage}
          onChange={handleSamplePercentageChange}
          disabled={!datasetSelected}
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Ratio - The proportion of samples in each batch to be replaced with
            their adversarial counterparts
          </strong>
        </label>
        <input
          id="ratio"
          type="number"
          step="0.1"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="ratio"
          value={ratio}
          onChange={handleRatioChange}
          disabled={!datasetSelected}
        />
      </div>
      <hr />
      <div>
        <label
          className="form-label"
          style={{
            display: "block",
            textAlign: "left",
            fontSize: "1.2rem",
            marginTop: "1rem",
          }}
        >
          <strong>Other Options (evasion attack)</strong>
        </label>
        <div className="additional-input-section">
          <div className="mb-3">
            <label
              className="form-label"
              style={{ display: "block", textAlign: "left" }}
            >
              <strong>Eps - Attack step size</strong>
            </label>
            <input
              id="eps"
              type="number"
              step="0.01"
              min="0.1"
              max="1"
              className="form-control"
              placeholder="eps"
              value={epsValue}
              onChange={handleEpsChange}
              disabled={!datasetSelected}
            />
          </div>
          <div className="mb-3">
            <label
              className="form-label"
              style={{ display: "block", textAlign: "left" }}
            >
              <strong>Eps Step - Step size of input variation</strong>
            </label>
            <input
              id="eps_step"
              type="number"
              step="0.01"
              min="0.1"
              max="1"
              className="form-control"
              placeholder="eps_step"
              value={epsStepValue}
              onChange={handleEpsStepChange}
              disabled={!datasetSelected}
            />
          </div>
          <div className="mb-3">
            <label
              className="form-label"
              style={{ display: "block", textAlign: "left" }}
            >
              <strong>
                Norm - The norm used for measuring the size of the perturbation
              </strong>
            </label>
            <select
              id="norm"
              className="form-select"
              value={normValue}
              onChange={handleNormChange}
              disabled={!datasetSelected}
            >
              <option value="inf">inf</option>
              <option value="1">1</option>
              <option value="2">2</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

AdversarialTrainerInput.propTypes = {
  epochs: PropTypes.string.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.string.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  evasionAttack: PropTypes.oneOf(["FGM", "PGD "]).isRequired,
  handleEvasionAttackChange: PropTypes.func.isRequired,
  samplePercentage: PropTypes.number.isRequired,
  handleSamplePercentageChange: PropTypes.func.isRequired,
  ratio: PropTypes.number.isRequired,
  handleRatioChange: PropTypes.func.isRequired,
  epsValue: PropTypes.number.isRequired,
  handleEpsChange: PropTypes.func.isRequired,
  epsStepValue: PropTypes.number.isRequired,
  handleEpsStepChange: PropTypes.func.isRequired,
  normValue: PropTypes.oneOf(["inf", "1", "2"]).isRequired,
  handleNormChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default AdversarialTrainerInput;
