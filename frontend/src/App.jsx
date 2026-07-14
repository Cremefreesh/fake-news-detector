import { useEffect, useState } from "react";

import AdminPage from "./pages/AdminPage";
import Home from "./pages/Home";

import "./styles/globals.css";
import "./styles/navigation.css";


function getCurrentPage() {
  return window.location.pathname === "/admin"
    ? "admin"
    : "home";
}


function App() {
  const [currentPage, setCurrentPage] = useState(
    getCurrentPage()
  );


  useEffect(() => {
    function handleBrowserNavigation() {
      setCurrentPage(getCurrentPage());
    }

    window.addEventListener(
      "popstate",
      handleBrowserNavigation
    );

    return () => {
      window.removeEventListener(
        "popstate",
        handleBrowserNavigation
      );
    };
  }, []);


  function navigate(path) {
    window.history.pushState({}, "", path);
    setCurrentPage(getCurrentPage());
  }


  return (
    <>
      <nav className="main-navigation">
        <button
          className="main-navigation-brand"
          type="button"
          onClick={() => navigate("/")}
        >
          TruthLens
        </button>

        <div className="main-navigation-links">
          <button
            className={
              currentPage === "home"
                ? "main-navigation-active"
                : ""
            }
            type="button"
            onClick={() => navigate("/")}
          >
            Detector
          </button>

          <button
            className={
              currentPage === "admin"
                ? "main-navigation-active"
                : ""
            }
            type="button"
            onClick={() => navigate("/admin")}
          >
            Admin
          </button>
        </div>
      </nav>

      {currentPage === "admin" ? (
        <AdminPage />
      ) : (
        <Home />
      )}
    </>
  );
}


export default App;