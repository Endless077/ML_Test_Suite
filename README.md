![Logo](https://github.com/Endless077/ML_Security_Project/blob/main/react_app/public/assets/art_logo.png)

# ML Test Suite 🛠️

This testing suite for machine learning is designed to assess and improve the robustness of models against adversarial attacks. It leverages the powerful [Adversarial Robustness Toolkit (ART)](https://github.com/Trusted-AI/adversarial-robustness-toolbox) library to provide a comprehensive set of tools and metrics for analyzing and mitigating model vulnerabilities.


## 🔑 Key Features

- **🔗 Easy Integration**: Compatible with various machine learning frameworks, including TensorFlow, PyTorch, and scikit-learn, for seamless integration into existing workflows.
- **⚔️ Attack Generation**: Utilizes advanced techniques to generate adversarial examples and test the model’s ability to withstand such inputs.
- **📊 Performance Metrics**: Provides a range of detailed metrics to measure the effectiveness of defense strategies and the overall robustness of models.
- **🛡️ Robustness Testing**: Evaluates model resilience to various types of adversarial attacks, including imperceptible perturbations and strategic manipulations.

![Example](https://github.com/Endless077/ML_Security_Project/blob/main/react_app/public/assets/art_schema.png)


## 🛠️ Installation

To run this program, you have two main options for installation: using a pre-configured script to set up the environment locally or using Docker.

### 🐍 Local Installation 🐍

1. **Install Prerequisites**:
   - Ensure you have the following installed on your system:
     - **GNOME**: Required for GUI-based components.
     - **npm**: Node package manager for managing JavaScript dependencies.
     - **Python**: Ensure you have Python installed (preferably Python 3.x).

2. **Set Up a Virtual Environment (Recommended)**:
   - Create a virtual environment to manage Python dependencies and avoid conflicts:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```
     - On macOS/Linux:
       ```bash
       source venv/bin/activate
       ```

3. **Run the Setup Script (First-Time Installation)**:
   - If this is your first time setting up the environment, run the `setup.sh` script to install all necessary dependencies:
     ```bash
     ./setup.sh
     ```
   - This script will:
     - Install Python packages from `requirements.txt`.
     - Install JavaScript dependencies using npm.

4. **Start the Application**:
   - After the initial setup, use the `start.sh` script to launch the application:
     ```bash
     ./start.sh
     ```

5. **Verify the Installation**:
   - Ensure that the application is running correctly by checking the output or running provided tests.

### 🐳 Docker Installation 🐳 

If you prefer to use Docker, follow these steps:

1. **Build the Docker Image**:
   - Use the provided Dockerfile to build the Docker image:
     ```bash
     docker build -t my_ml_app .
     ```

2. **Run the Docker Container**:
   - Start a container from the built image:
     ```bash
     docker run -it --rm my_ml_app
     ```

3. **Access the Application**:
   - Once the container is running, you can interact with the application as specified in the documentation or example scripts.

### ⚠️ Additional Notes ⚠️

- **Dependencies**: Ensure all required software (GNOME, npm, Python) is installed before running the setup scripts.
- **Custom Configuration**: For any additional configuration or environment variables, refer to the `README` or `INSTALL.md` file.


## 📜 API Reference

You can view the API documentation using FastAPI by visiting the **/docs** endpoint of your server (i.e., [http://localhost:8000/docs](http://localhost:8000/docs)). This interactive interface provides a comprehensive list of available APIs, including details on each supported request, required parameters, allowed HTTP methods, and expected responses. It's an invaluable tool for quickly exploring and understanding the functionality offered by your APIs without the need to manually reference static documentation.


## 🙏 Acknowledgements

### FastAPI 🚀

FastAPI is a modern web framework for building APIs with Python 3.7+ based on standard Python type hints. It offers high performance with automatic interactive documentation (Swagger UI), WebSocket support, GraphQL integration, CORS middleware, OAuth2 authentication, and more.

[More information here](https://github.com/tiangolo/fastapi)

### Adversarial Robustness Toolkit (ART) 🛡️

The Adversarial Robustness Toolkit (ART) is an open-source library designed to enhance the security of machine learning models against adversarial attacks. Developed by Trusted AI, ART provides a robust suite of tools for evaluating model vulnerability, implementing defense strategies, and improving adversarial robustness. It supports a wide range of attack methods and defensive techniques and is compatible with popular machine learning frameworks like TensorFlow, PyTorch, and scikit-learn.

#### 🗡️ Categories of Attacks 🗡️

- **Evasion Attacks**:
  - **Description**: Evasion attacks aim to deceive the model during inference by creating manipulated inputs that cause classification errors. For example, a slightly altered image might be misclassified as a different object.
  - **Examples**: 
    - Gradient-based attacks (Fast Gradient Sign Method, Projected Gradient Descent)

- **Poisoning Attacks**:
  - **Description**: Poisoning attacks target the training data by injecting malicious data to degrade the model's performance or induce undesirable behaviors.
  - **Examples**:
    - Label flipping attacks
    - Data injection attacks

- **Inference Attacks**:
  - **Description**: Inference attacks attempt to extract sensitive information about the training data or the model itself. This can include reconstructing private data or revealing specific model characteristics.
  - **Examples**:
    - Model extraction attacks
    - Membership inference attacks

- **Backdoor Attacks**:
  - **Description**: Backdoor attacks introduce a "trojan horse" into the model, causing it to behave in a specific way when presented with a particular trigger while maintaining overall good performance.
  - **Examples**:
    - Trigger-based backdoor attacks with visible or invisible triggers

#### 🛡️ Categories of Defenses 🛡️

- **Adversarial Training**:
  - **Description**: Adversarial training involves training the model with adversarially generated examples, thereby improving its robustness against similar attacks during inference.
  - **Examples**:
    - Integrating adversarial examples into the training set

- **Input Preprocessing**:
  - **Description**: Input preprocessing techniques aim to mitigate the effects of adversarial attacks by transforming or filtering inputs before they reach the model.
  - **Examples**:
    - Noise reduction
    - Image normalization
    - Input transformations

- **Robust Optimization**:
  - **Description**: Robust optimization involves modifying the training process to enhance the model's resilience to adversarial perturbations.
  - **Examples**:
    - Robust optimization techniques such as robustness-based regularization

- **Certified Defenses**:
  - **Description**: Certified defenses provide formal guarantees of the model's robustness against specific classes of adversarial attacks, offering a certain level of mathematical security.
  - **Examples**:
    - Robustness certification through techniques such as training with robustness constraints

- **Anomaly Detection**:
  - **Description**: Anomaly detection systems identify and manage inputs that deviate from normal model behavior, often used to detect and handle adversarial inputs.
  - **Examples**:
    - Anomaly detection algorithms based on statistical or machine learning methods

[More Information](https://adversarial-robustness-toolbox.org/)

### React ⚛️

React is a JavaScript library for building user interfaces, developed by Facebook. It is known for creating reusable components that efficiently manage application state. React uses a component-based approach to build dynamic and responsive user interfaces.

[More information here](https://reactjs.org/)

### Vite ⚡

Vite is a fast build tool for modern web development. It is designed to speed up the development server and hot module replacement (HMR) thanks to its ESModule support, enabling JavaScript module imports without a build step.

[More information here](https://github.com/vitejs/vite)

### Other Various Utilities 🔧

In the realm of modern application development, there are numerous useful tools and libraries that enhance productivity and efficiency. Some of these include:

- **[Axios](https://github.com/axios/axios)**: A promise-based HTTP client for making AJAX requests.
- **[Bootstrap](https://getbootstrap.com/)**: CSS framework for building responsive and styled user interfaces.

These tools and technologies are widely adopted in the software development community to improve the quality, maintainability, and performance of modern applications.


## 💾 License

This project is licensed under the GNU General Public License v3.0.

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

![Static Badge](https://img.shields.io/badge/UniSA-WTFunko-red?style=plastic)


## 🖐 Authors

**Contributors:**
- [Fulvio Serao](https://github.com/Fulvioserao99)

**Project Manager:**
- [Antonio Garofalo](https://github.com/Endless077)


## 🔔 Support

For support, email [antonio.garofalo125@gmail.com](mailto:antonio.garofalo125@gmail.com) or contact the project contributors.


### 📝 Documentation

See the documentation project **[here](https://github.com/Endless077/ML_Test_Suite/blob/main/docs.pdf)**.
