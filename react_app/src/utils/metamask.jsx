// MetaMask
import React, { createContext, useContext, useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import Swal from "sweetalert2";

const MetaMaskContext = createContext();
export const useMetaMask = () => useContext(MetaMaskContext);

export const MetaMaskProvider = ({ children, dappMetadata }) => {
  const [userLogged, setUserLogged] = useState(false);
  const [wallet, setWallet] = useState(null);
  const [token, setToken] = useState(null);

  /* ******************************************************************************************* */

  useEffect(() => {
    checkConnection();

    if (window.ethereum) {
      window.ethereum.on("accountsChanged", checkConnection);
      window.ethereum.on("chainChanged", checkConnection);
    }

    return () => {
      if (window.ethereum) {
        window.ethereum.removeListener("accountsChanged", checkConnection);
        window.ethereum.removeListener("chainChanged", checkConnection);
      }
    };
  }, []);

  /* ******************************************************************************************* */

  const checkConnection = async () => {
    if (window.ethereum) {
      try {
        const accounts = await window.ethereum.request({
          method: "eth_accounts",
        });

        if (accounts.length === 0) {
          logout();
        } else {
          const savedWallet = localStorage.getItem("wallet");
          const savedToken = localStorage.getItem("token");

          if (savedWallet && savedToken && accounts.includes(savedWallet)) {
            setUserLogged(true);
            setWallet(savedWallet);
            setToken(savedToken);
          } else {
            logout();
            Swal.fire({
              icon: "error",
              title: "You are not logged in",
              text: "The wallet connected to MetaMask is offline.",
            });
          }
        }
      } catch (error) {
        console.error("Error checking MetaMask connection:", error);
        Swal.fire({
          icon: "error",
          title: "MetaMask Error",
          html: `
          <div style="text-align: center;">
            <p>An error occurred while checking the MetaMask connection.</p>
            <p style="white-space: pre-wrap;">${error.message}</p>
          </div>
        `,
        });
      }
    } else {
      logout();
      Swal.fire({
        icon: "error",
        title: "MetaMask not found",
        text: "Please install MetaMask and try again.",
      });
    }
  };

  const connect = async () => {
    if (window.ethereum) {
      try {
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });

        if (accounts.length > 0) {
          const account = accounts[0];
          const savedToken = uuidv4();

          localStorage.setItem("wallet", account);
          localStorage.setItem("token", savedToken);

          setUserLogged(true);
          setWallet(account);
          setToken(savedToken);

          Swal.fire({
            icon: "success",
            title: "Connected",
            text: `Connected to MetaMask account ${account}`,
          });
        }
      } catch (error) {
        console.error("Error connecting to MetaMask:", error);
        Swal.fire({
          icon: "error",
          title: "MetaMask Connection Error",
          html: `
          <div style="text-align: center;">
            <p>An error occurred while checking the MetaMask connection.</p>
            <p style="white-space: pre-wrap;">${error.message}</p>
          </div>
        `,
        });
      }
    } else {
      Swal.fire({
        icon: "error",
        title: "MetaMask not found",
        text: "Please install MetaMask and try again.",
      });
    }
  };

  const logout = () => {
    setUserLogged(false);
    setWallet(null);
    setToken(null);
    localStorage.removeItem("wallet");
    localStorage.removeItem("token");
  };

  /* ******************************************************************************************* */

  return (
    <MetaMaskContext.Provider
      value={{ userLogged, wallet, token, dappMetadata, checkConnection, connect, logout }}
    >
      {children}
    </MetaMaskContext.Provider>
  );
};
