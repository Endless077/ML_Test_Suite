// Functions
import { config } from "./config";

import Swal from "sweetalert2";
import withReactContent from "sweetalert2-react-content";

// URL API
const apiUrl = `${config.api_url}:${config.api_port}`;

// Dialog Object
const MySwal = withReactContent(Swal);

/* ********************************************************************************************* */

async function fetchData(endpoint, method, headers = null, body = null) {
  const url = `http://${apiUrl}${endpoint}`;

  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  const otherHeaders = headers
    ? { ...defaultHeaders, ...headers }
    : defaultHeaders;

  const options = {
    method: method,
    headers: otherHeaders,
    body: body ? JSON.stringify(body) : null,
  };

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return response;
}

/* ********************************************************************************************* */

export async function uploadModel(filename, model) {
  const endpoint = config.endpoints.uploadModel;
  const method = "POST";

  const formData = new FormData();
  formData.append("model", model);
  formData.append("filename", filename);

  const url = `http://${apiUrl}${endpoint}`;
  const options = {
    method: method,
    body: formData,
  };

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return response;
}

export async function uploadDataset(directoryname, dataset) {
  const endpoint = config.endpoints.uploadDataset;
  const method = "POST";

  const formData = new FormData();
  formData.append("zipfile", dataset);
  formData.append("directoryname", directoryname);

  const url = `http://${apiUrl}${endpoint}`;
  const options = {
    method: method,
    body: formData,
  };

  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return await response.json();
}

export async function performAttack(attack, attackType, attackModel) {
  const endpoint = config.endpoints.attacks[attack].endpoint.replace(
    "{attack_type}",
    attackType
  );
  const method = config.endpoints.attacks[attack].method;
  return await fetchData(endpoint, method, undefined, attackModel)
    .then((response) => response.json())
    .catch((error) => {
      console.error(error);
      throw error;
    });
}

export async function performDefense(defense, defenseType, defenseModel) {
  const endpoint = config.endpoints.defenses[defense].endpoint.replace(
    "{defense_type}",
    defenseType
  );
  const method = config.endpoints.defenses[defense].method;
  return await fetchData(endpoint, method, undefined, defenseModel)
    .then((response) => response.json())
    .catch((error) => {
      console.error(error);
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
    title: dialogTitle,
    text: dialogText,
    icon: "error",
  });
};

export const showSuccessAlert = async (result, test, navigate) => {
  const redirectResult = await MySwal.fire({
    title: "Success",
    text: "Do you want to be redirected to the Results page?",
    icon: "success",
    showCancelButton: true,
    confirmButtonText: "Yes",
    cancelButtonText: "No",
  });
  if (redirectResult.isConfirmed) {
    localStorage.setItem("latestTest", test);
    localStorage.setItem("latestResult", result);
    navigate("/results", { state: { latestTest: test, latestResult: result } });
  }
};

/* ********************************************************************************************* */

const startAttackProcess = async (
  attack,
  attackType,
  attackModel,
  navigate
) => {
  try {
    const choice = await MySwal.fire({
      icon: "info",
      title: `Do you want to proceed with ${attack} ${attackType} attack?`,
      showCancelButton: true,
      confirmButtonText: "Yes",
      cancelButtonText: "No",
    });

    if (choice.isConfirmed) {
      MySwal.fire({
        icon: "warning",
        title: `Elaboration ${attack} ${attackType} test in progress`,
        text: "Check progress in your console",
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading();
        },
      });

      performAttack(attack, attackType, attackModel)
        .then((fatchResult) => {
          return showSuccessAlert(
            fatchResult,
            `${attack} (${attackType})`,
            navigate
          );
        })
        .catch((error) => {
          console.error(error);
          showFailAlert("Fetch Error", error.message);
        });
    }
  } catch (error) {
    console.error(error);
    showFailAlert("Server Error", error.message);
  }
};

const startDefenseProcess = async (
  defense,
  defenseType,
  defenseModel,
  navigate
) => {
  try {
    const choice = await MySwal.fire({
      icon: "info",
      title: `Do you want to proceed with ${defense} ${defenseType} defense?`,
      showCancelButton: true,
      confirmButtonText: "Yes",
      cancelButtonText: "No",
    });

    if (choice.isConfirmed) {
      MySwal.fire({
        icon: "warning",
        title: `Elaboration ${defense} ${defenseType} test in progress`,
        text: "Check progress in your console",
        allowOutsideClick: false,
        didOpen: () => {
          Swal.showLoading();
        },
      });

      performDefense(defense, defenseType, defenseModel)
        .then((fatchResult) => {
          return showSuccessAlert(
            fatchResult,
            `${defense} (${defenseType})`,
            navigate
          );
        })
        .catch((error) => {
          console.error(error);
          showFailAlert("Fetch Error", error.message);
        });
    }
  } catch (error) {
    console.error("Server Error processing:", error);
    showFailAlert("Server Error", error.message);
  }
};

export { startAttackProcess, startDefenseProcess };
