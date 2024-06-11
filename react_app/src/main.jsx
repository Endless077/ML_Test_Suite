import React from "react";
import ReactDOM from "react-dom/client";

// Index Default CSS
import "./index.css";

// Config.js
import { config } from "./utils/config.js";

// Material Design Bootstrap (MDB)
import "mdb-react-ui-kit/dist/css/mdb.min.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

/* ********************************************************************************************* */

// Main Page
import Results from "./pages/results.jsx";
import HomePage from "./pages/homepage.jsx";

// Attack Pages
import FirstGradientMethod from "./pages/attacks/FirstGradientMethod.jsx";
import ProjectedGradientDescent from "./pages/attacks/ProjectedGradientDescent.jsx";
import CopycatCNN from "./pages/attacks/CopycatCNN.jsx";
import MIFace from "./pages/attacks/MIFace.jsx";
import CleanLabelBackdoor from "./pages/attacks/CleanLabelBackdoor.jsx";
import SimpleBackdoor from "./pages/attacks/SimpleBackdoor.jsx";

// Defense Pages
import ActivationDefense from "./pages/defenses/ActivationDefense.jsx";
import ReverseSigmoid from "./pages/defenses/ReverseSigmoid.jsx";
import TotalVarMin from "./pages/defenses/TotalVarMin.jsx";
import AdversarialTrainer from "./pages/defenses/AdversarialTrainer.jsx";
import STRongIntentionalPerturbation from "./pages/defenses/STRongIntentionalPerturbation.jsx";

import {
  createBrowserRouter,
  RouterProvider,
  Navigate,
} from "react-router-dom";

// Define Paths
const paths = {
  results: "/results",
  homepage: "/homepage",
  attack: {
    fgm: "/attack/FGM",
    pgd: "/attack/PGD",
    copycatCNN: "/attack/CopycatCNN",
    miFace: "/attack/MIFace",
    cleanLabelBackdoor: "/attack/CleanLabelBackdoor",
    simpleBackdoor: "/attack/SimpleBackdoor",
  },
  defense: {
    activationDefense: "/defense/ActivationDefense",
    reverseSigmoid: "/defense/ReverseSigmoid",
    totalVarMin: "/defense/TotalVarMin",
    adversarialTrainer: "/defense/AdversarialTrainer",
    strongIntentionalPerturbation: "/defense/STRongIntentionalPerturbation",
  },
};

// Definine Routes
const routes = [
  { path: "/", element: <Navigate to={paths.homepage} /> },
  { path: paths.results, element: <Results /> },
  { path: paths.homepage, element: <HomePage /> },
  { path: paths.attack.fgm, element: <FirstGradientMethod /> },
  { path: paths.attack.pgd, element: <ProjectedGradientDescent /> },
  { path: paths.attack.copycatCNN, element: <CopycatCNN /> },
  { path: paths.attack.miFace, element: <MIFace /> },
  { path: paths.attack.cleanLabelBackdoor, element: <CleanLabelBackdoor /> },
  { path: paths.attack.simpleBackdoor, element: <SimpleBackdoor /> },
  { path: paths.defense.activationDefense, element: <ActivationDefense /> },
  { path: paths.defense.reverseSigmoid, element: <ReverseSigmoid /> },
  { path: paths.defense.totalVarMin, element: <TotalVarMin /> },
  { path: paths.defense.adversarialTrainer, element: <AdversarialTrainer /> },
  {
    path: paths.defense.strongIntentionalPerturbation,
    element: <STRongIntentionalPerturbation />,
  },
];

// Create a BrowserRouter
const router = createBrowserRouter(routes);

// Initialize the WebApp
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
