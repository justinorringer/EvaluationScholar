import React from "react";
import { NavLink } from "react-router-dom";

//Function to create an HTML representation of a Header/Navbar for the application
//which includes routes to the different pages of the application.

function Header() {
  return (
    <div className="navigation">
      <nav className="navbar static-top navbar-expand-sm navbar-dark bg-dark">
        <div className="container">
          <NavLink className="navbar-brand" to="/">
            EvaluationScholar
          </NavLink>
          <div>
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <NavLink className="nav-link" to="/">
                  Query
                  <span className="sr-only">(current)</span>
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/input">
                  Input
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </div>
  );
}

export default Header;