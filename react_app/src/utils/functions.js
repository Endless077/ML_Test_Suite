import { config } from './config'

import Swal from 'sweetalert2';
import withReactContent from 'sweetalert2-react-content';

// URL API
const apiUrl = `${config.api_url}:${config.api_port}`;

// Dialog Object
const MySwal = withReactContent(Swal);

/* ********************************************************************************************* */

async function fetchData(endpoint, method, body = null) {
  const url = `${apiUrl}${endpoint}`;

  const options = {
    method: method,
    headers: {
      'Content-Type': 'application/json'
    },
    body: body ? JSON.stringify(body) : null
  };

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Error: ${response.statusText}`);
  }
  return response.json();
}

/* ********************************************************************************************* */

export async function performAttack(attackType, attackModel) {
  const endpoint = config.endpoints.attacks[attackType].endpoint.replace("{attack_type}", attackType);
  const method = config.endpoints.attacks[attackType].method;
  return await fetchData(endpoint, method, attackModel)
    .then(response => {
      return response; 
    })
    .catch(error => {
      console.error("Error:", error);
      throw error;
    });
}

export async function performDefense(defenseType, defenseModel) {
  const endpoint = config.endpoints.defenses[defenseType].endpoint.replace("{defense_type}", defenseType);
  const method = config.endpoints.defenses[defenseType].method;
  return await fetchData(endpoint, method, defenseModel)
    .then(response => {
      return response; 
    })
    .catch(error => {
      console.error("Error:", error);
      throw error;
    });
}

/* ********************************************************************************************* */

export const showErrorAlert = (errors) => {
  const alertContent = errors.map((error) => `<li>${error}</li>`).join("");

  MySwal.fire({
    title: "Oops...",
    html: `<div style="text-align: left;">Correct the following errors:<ul>${alertContent}</ul></div>`,
    icon: "error",
    confirmButtonText: "OK",
    customClass: {
      container: "custom-alert-container",
      title: "custom-alert-title",
      htmlContainer: "custom-alert-html-container",
    },
  });
};

export const showFailAlert = (dialogTitle, dialogText) => {
  return MySwal.fire({
    title: title,
    text: dialogText,
    icon: 'error'
  });
};

export const showSuccessAlert = (result, test, navigate) => {
  return MySwal.fire({
    title: 'Success',
    text: 'Do you want to be redirected to the Results page?',
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'Yes',
    cancelButtonText: 'No'
  }).then((redirectResult) => {
    if (redirectResult.isConfirmed) {
      localStorage.setItem('latestResult', JSON.stringify(result));
      localStorage.setItem('latestTest', test);
      navigate("/results")
    }
  });
};

/* ********************************************************************************************* */

const startAttackProcess = async (attackType, attackModel, navigate) => {
  try {
    const choice = await MySwal.fire({
      title: 'Do you want to proceed with ${attackType}?',
      icon: "info",
      showCancelButton: true,
      confirmButtonText: 'Yes',
      cancelButtonText: 'No'
    });

    if (choice.isConfirmed) {
      MySwal.fire({
        title: 'Elaboration ${attackType} test in progress',
        text: 'Check progress in your console',
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading();
        }
      });

      performAttack(attackType, attackModel)
        .then((fatchResult) => {
          return showSuccessAlert(fatchResult, attack_type, navigate)})
        .catch((error) => {
          console.error('Fetch Error:', error);
          showFailAlert('Fetch Error', `An error occurred: ${error.message}`);
        });
    }
  } catch (error) {
    console.error('Server Error processing:', error);
    showFailAlert('Server Error', `An error occurred: ${error.message}`);
  }
};

const startDefenseProcess = async (defenseType, attackModel, navigate) => {
  try {
    const choice = await MySwal.fire({
      title: 'Do you want to proceed with ${defenseType}?',
      icon: "info",
      showCancelButton: true,
      confirmButtonText: 'Yes',
      cancelButtonText: 'No'
    });

    if (choice.isConfirmed) {
      MySwal.fire({
        title: 'Elaboration ${defenseType} test in progress',
        text: 'Check progress in your console',
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading();
        }
      });

      performAttack(defenseType, defenseModel)
        .then((fatchResult) => {
          return showSuccessAlert(fatchResult, defenseType, navigate)})
        .catch((error) => {
          console.error('Fetch Error:', error);
          showFailAlert('Fetch Error', `An error occurred: ${error.message}`);
        });
    }
  } catch (error) {
    console.error('Server Error processing:', error);
    showFailAlert('Server Error', `An error occurred: ${error.message}`);
  }
};

export { startAttackProcess, startDefenseProcess };