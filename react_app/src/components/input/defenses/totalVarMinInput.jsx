import React from "react";
import PropTypes from "prop-types";

const TotalVarMinInput = ({
  epochs,
  handleEpochsChange,
  batchSize,
  handleBatchSizeChange,
  evasionAttack,
  handleEvasionAttackChange,
  samplePercentage,
  handleSamplePercentageChange,
  prob,
  handleProbChange,
  normInt,
  handleNormIntChange,
  lamb,
  handleLambChange,
  solver,
  handleSolverChange,
  maxIter,
  handleMaxIterChange,
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
          <strong>Prob - Probability of the Bernoulli distribution</strong>
        </label>
        <input
          id="prob"
          type="number"
          step="0.01"
          min="0.1"
          max="1"
          className="form-control"
          placeholder="prob"
          value={prob}
          onChange={handleProbChange}
          disabled={!datasetSelected}
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Norm - The norm</strong>
        </label>
        <input
          id="norm"
          type="text"
          className="form-control"
          placeholder="norm"
          value={normInt}
          onChange={handleNormIntChange}
          disabled={!datasetSelected}
        />
      </div>

      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Lamb - The lambda parameter in the objective function</strong>
        </label>
        <input
          id="lamb"
          type="text"
          className="form-control"
          placeholder="lamb"
          value={lamb}
          onChange={handleLambChange}
          disabled={!datasetSelected}
        />
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>Solver - Which solver to use</strong>
        </label>
        <select
          id="solver"
          className="form-select"
          value={solver}
          onChange={handleSolverChange}
          disabled={!datasetSelected}
        >
          <option value="L-BFGS-B">L-BFGS-B</option>
          <option value="CG">CG</option>
          <option value="Newton-CG">Newton-CG</option>
        </select>
      </div>
      <div className="mb-3">
        <label
          className="form-label"
          style={{ display: "block", textAlign: "left" }}
        >
          <strong>
            Max Iter - Maximum number of iterations when performing optimizatio
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

TotalVarMinInput.propTypes = {
  epochs: PropTypes.string.isRequired,
  handleEpochsChange: PropTypes.func.isRequired,
  batchSize: PropTypes.string.isRequired,
  handleBatchSizeChange: PropTypes.func.isRequired,
  evasionAttack: PropTypes.oneOf(["FGM", "PGD "]).isRequired,
  handleEvasionAttackChange: PropTypes.func.isRequired,
  samplePercentage: PropTypes.number.isRequired,
  handleSamplePercentageChange: PropTypes.func.isRequired,
  prob: PropTypes.number.isRequired,
  handleProbChange: PropTypes.func.isRequired,
  normInt: PropTypes.number.isRequired,
  handleNormIntChange: PropTypes.func.isRequired,
  lamb: PropTypes.number.isRequired,
  handleLambChange: PropTypes.func.isRequired,
  solver: PropTypes.oneOf(["L-BFGS-B", "CG", "Newton-CG"]).isRequired,
  handleSolverChange: PropTypes.func.isRequired,
  maxIter: PropTypes.number.isRequired,
  handleMaxIterChange: PropTypes.func.isRequired,
  epsValue: PropTypes.number.isRequired,
  handleEpsChange: PropTypes.func.isRequired,
  epsStepValue: PropTypes.number.isRequired,
  handleEpsStepChange: PropTypes.func.isRequired,
  normValue: PropTypes.oneOf(["inf", "1", "2"]).isRequired,
  handleNormChange: PropTypes.func.isRequired,
  datasetSelected: PropTypes.bool.isRequired,
};

export default TotalVarMinInput;
