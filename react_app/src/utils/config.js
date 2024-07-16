// Config
export const config = {
  api_url: "localhost",
  api_port: 8000,
  endpoints: {
    uploadModel: "/upload/model",
    uploadDir: "/upload/directory",
    attacks: {
      evasion: {
        endpoint: "/attack/evasion/{attack_type}",
        method: "POST"
      },
      extraction: {
        endpoint: "/attack/extraction/{attack_type}",
        method: "POST"
      },
      inference: {
        endpoint: "/attack/inference/{attack_type}",
        method: "POST"
      },
      poisoning: {
        endpoint: "/attack/poisoning/{attack_type}",
        method: "POST"
      }
    },
    defenses: {
      detector: {
        endpoint: "/defense/detector/{defense_type}",
        method: "POST"
      },
      postprocessor: {
        endpoint: "/defense/postprocessor/{defense_type}",
        method: "POST"
      },
      preprocessor: {
        endpoint: "/defense/preprocessor/{defense_type}",
        method: "POST"
      },
      trainer: {
        endpoint: "/defense/trainer/{defense_type}",
        method: "POST"
      },
      transformer: {
        endpoint: "/defense/transformer/{defense_type}",
        method: "POST"
      }
    }
  }
};
