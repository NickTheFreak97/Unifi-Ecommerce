import { Outlet, Link } from "react-router";
import { AppBar, Toolbar } from "@mui/material";
import { useAuth, getAccessToken } from "./context/AuthContext";

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
                        <li>
                            { userIdentity.user.email }
                        </li>
                }
            </ul>
        </Toolbar>
      </AppBar>

      <Outlet />
    </>
  );
}