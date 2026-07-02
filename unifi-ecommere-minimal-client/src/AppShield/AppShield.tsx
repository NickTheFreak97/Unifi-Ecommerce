import { Outlet, Link } from "react-router";
import { AppBar, Toolbar } from "@mui/material";
import { useAuth, getAccessToken } from "../context/AuthContext";

import './appshield.css'

export default function AppShield() {
    const userIdentity = useAuth();

  return (
    <>
      <AppBar position="static">
        <Toolbar>
            <ul>
                <li><Link to='/'>Home</Link></li>
                
                {
                    !userIdentity.isLoading && !!userIdentity.user &&
                    <>
                        <li>
                          { userIdentity.user.username }
                        </li>
                        <li>
                            Log out
                        </li>
                    </>
                }
            </ul>
        </Toolbar>
      </AppBar>

      <Outlet />
    </>
  );
}