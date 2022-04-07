import React from "react";
import { NavLink } from "react-router-dom";

//Function to create an HTML representation of a Header/Navbar for the application
//which includes routes to the different pages of the application.

function Header() {
  return (
    <div className="navigation">
      <nav className="navbar fixed-top navbar-expand-sm navbar-dark bg-dark">
        <div className="container">
          <NavLink className="navbar-brand" to="/">
            EvaluationScholar
          </NavLink>
          <div>
            <ul className="navbar-nav ml-auto">
              <li className="nav-item">
                <NavLink className="nav-link" to="/papers">
                  Papers
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/issues">
                  Issues
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/tasks">
                  Tasks
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/tags">
                  Tags
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/visualize">
                  Visualize
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