import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";


import Home from "./routes/Home";
import Root from './routes/Root'
import NotFound from "./routes/NotFound";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";


const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <NotFound />,
    children: [
      { 
        element: <ProtectedRoute />,
        children: [
          { index: true, element: <Home /> }
        ]
      },
    ],
  },
]);

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});


createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <RouterProvider router={router} />
        </ThemeProvider>
      </AuthProvider>
  </StrictMode>,
);
