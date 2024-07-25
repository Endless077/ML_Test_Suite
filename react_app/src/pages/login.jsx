// Login
import Navbar from "../components/header";
import Footer from "../components/footer";

import { useMetaMask } from "../utils/metamask.jsx";
import metamaskLogo from "/assets/metamask.png";
import { useNavigate } from "react-router-dom";

let pageTitle = "Adversarial Robustness Toolbox";

function Login() {
  const {
    userLogged,
    wallet,
    token,
    dappMetadata,
    checkConnection,
    connect,
    logout
  } = useMetaMask();

  const navigate = useNavigate()
  
  /* ********************************************************************************************* */

  const handleLogin = async () => {
    connect()
  };

  const handleLogout = () => {
    logout()
  };

  const openMetamask = () => {
    window.open("https://metamask.io/", "_blank");
  };

  /* ********************************************************************************************* */

  return (
    <div id="root">
      <Navbar pageTitle={pageTitle} />
      <div className="page-content">
        <h1 className="title">Login with Metamask</h1>{" "}
        <p className="description">
          Our app was initially designed to be used as a DApp, so we OBVIOUSLY
          require a Metamask account linked to an Ethereum wallet.
        </p>
        <hr />
        <div
          className="metamask-button-container"
          style={{
            display: "flex",
            justifyContent: "center",
            width: "100%",
            marginTop: "20px",
          }}
        >
          <button
            className={`btn ${userLogged ? "btn-success" : "btn-primary"}`}
            onClick={userLogged ? openMetamask : handleLogin}
            style={{
              width: "330px",
              padding: "15px 25px",
              fontSize: "1rem",
              borderRadius: "5px",
              color: "#ffffff",
              cursor: "pointer",
              transition: "background-color 0.3s",
              backgroundColor: userLogged ? "#28a745" : "#3c3c3d",
              border: "none",
              marginTop: userLogged ? "0" : "20px",
              fontWeight: "bold",
            }}
          >
            <img
              src={metamaskLogo}
              alt="Metamask Icon"
              className="metamask-icon"
              style={{ width: "24px", height: "24px", marginRight: "10px" }}
            />
            {userLogged ? "Open Metamask" : "Connect with MetaMask"}
          </button>
        </div>
        <div
          className="login-status"
          style={{ marginTop: "20px", fontSize: "1.2em", color: "#333" }}
        >
          {userLogged ? (
            <>
              <p
                style={{
                  fontWeight: "bold",
                  color: "#333",
                  textAlign: "center",
                }}
              >
                Etherium Wallet connected
                <br />
                {wallet}
              </p>
              <div
                className="button-group"
                style={{
                  marginTop: "10px",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                }}
              >
                <button
                  className="btn btn-primary"
                  onClick={() => navigate("/homepage")}
                  style={{ marginTop: "10px" }}
                >
                  Go to Homepage
                </button>
                <button
                  className="btn btn-danger"
                  onClick={handleLogout}
                  style={{ marginTop: "10px" }}
                >
                  Logout
                </button>
              </div>
            </>
          ) : (
            <p style={{ fontWeight: "bold" }}>
              No Etherium Wallet is connected
            </p>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Login;
