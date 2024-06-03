import React from "react";
import PropTypes from "prop-types";

const MIFaceInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  maxIter,
  handleMaxIterChange,
  windowLength,
  handleWindowLengthChange,
  threshold,
  handleThresholdChange,
  learningRate,
  handleLearningRateChange,
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
          <strong>
            Max Iter - Maximum number of gradient descent iterations for the
            model inversion
          </strong>
        </label>
        <input
          id="max_iter"
          type="text"
          className="form-control"
          placeholder="max_iter"
          value={maxIter}
          onChange={handleMaxIterChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Window Length - Length of window for checking whether descent should
            be aborted
          </strong>
        </label>
        <input
          id="window_length"
          type="text"
          className="form-control"
          placeholder="window_length"
          value={windowLength}
          onChange={handleWindowLengthChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Threshold - Threshold for descent stopping criterion</strong>
        </label>
        <input
          id="threshold"
          type="text"
          className="form-control"
          placeholder="threshold"
          value={threshold}
          onChange={handleThresholdChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Learning Rate - The learning rate</strong>
        </label>
        <input
          id="learning_rate"
          type="text"
          className="form-control"
          placeholder="learning_rate"
          value={learningRate}
          onChange={handleLearningRateChange}
          disabled={!datasetSelected}
          pattern="[0-9]*"
        />
      </div>
    </div>
  );
};

MIFaceInput.propTypes = {
  epochs: PropTypes.string.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.string.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  maxIter: PropTypes.string.isRequired,
  handleMaxIterChange: PropTypes.func.isRequired,
  windowLength: PropTypes.string.isRequired,
  handleWindowLengthChange: PropTypes.func.isRequired,
  threshold: PropTypes.string.isRequired,
  handleThresholdChange: PropTypes.func.isRequired,
  learningRate: PropTypes.string.isRequired,
  handleLearningRateChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default MIFaceInput;
