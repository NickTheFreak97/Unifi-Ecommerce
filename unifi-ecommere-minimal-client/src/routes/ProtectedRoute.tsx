import React, { useEffect, useState } from "react";
import { Outlet } from "react-router";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import { useAuth } from "../context/AuthContext";

export const ProtectedRoute: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!isLoading) {
      setOpen(!isAuthenticated);
    }
  }, [isLoading, isAuthenticated]);

  if (isLoading) {
    return null;
  }

  return (
    <>
      <Outlet />

      <Snackbar
        open={open}
        autoHideDuration={6000}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
        onClose={() => setOpen(false)}
      >
        <Alert severity="warning" variant="filled" sx={{ width: "100%" }}>
          No user authentication detected, requests from this route will fail
        </Alert>
      </Snackbar>
    </>
  );
};