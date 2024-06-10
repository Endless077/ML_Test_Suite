import { config } from './config'

// Url API
const apiUrl = `${config.api_url}:${config.api_port}`;

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

async function performAttack(attackType, attackModel) {
  const endpoint = config.endpoints.attacks[attackType].endpoint.replace("{attack_type}", attackType);
  const method = config.endpoints.attacks[attackType].method;
  return fetchData(endpoint, method, attackModel)
    .then(response => {
      // Redirect to the results page with the response data
      window.location.href = `/result?data=${encodeURIComponent(JSON.stringify(response))}`;
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

async function performDefense(defenseType, defenseModel) {
  const endpoint = config.endpoints.defenses[defenseType].endpoint.replace("{defense_type}", defenseType);
  const method = config.endpoints.defenses[defenseType].method;
  return fetchData(endpoint, method, defenseModel)
    .then(response => {
      // Redirect to the results page with the response data
      window.location.href = `/result?data=${encodeURIComponent(JSON.stringify(response))}`;
    })
    .catch(error => {
      console.error("Error:", error);
    });
}

export { performAttack, performDefense };
