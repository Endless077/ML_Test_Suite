import React from "react";
import PropTypes from "prop-types";

const STRIPInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  poisonPercentage,
  handlePoisonPercentageChange,
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
          <strong>Poison Attack</strong>
        </label>
        <select
          id="poison_attack"
          className="form-select"
          value={poisonAttack}
          onChange={handlePoisonAttackChange}
          disabled={!datasetSelected}
        >
          <option value="cleanlabel">Clean Label Backdoor</option>
          <option value="simple">Simple Backdoor</option>
        </select>
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Poison Percentage - Percentage of poisoned dataset</strong>
        </label>
        <input
          id="poison_percentage"
          type="number"
          step="0.01"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="poison_percentage"
          value={poisonPercentage}
          onChange={handlePoisonPercentageChange}
          disabled={!datasetSelected}
        />
      </div>
    </div>
  );
};

STRIPInput.propTypes = {
  epochs: PropTypes.string.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.string.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  poisonAttack: PropTypes.string.isRequired,
  handlePoisonAttackChange: PropTypes.func.isRequired,
  poisonPercentage: PropTypes.string.isRequired,
  handlePoisonPercentageChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default STRIPInput;
