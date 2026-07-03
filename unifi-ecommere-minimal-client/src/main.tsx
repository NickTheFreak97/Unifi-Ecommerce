import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { createBrowserRouter } from "react-router";
import { RouterProvider } from "react-router/dom";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";


import Home from "./routes/Home";
import NotFound from "./routes/NotFound";
import { ProtectedRoute } from "./routes/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";
import CreateUser from "./routes/Signup/CreateUser";
import theme from "./theme/Theme";
import AppShield from "./AppShield/AppShield";
import Login from "./Login/Login";
import Logout from "./routes/Logout/Logout";
import ListAllUsers from "./routes/ListAllUsers";

const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShield />,
    errorElement: <NotFound />,
    children: [
      { 
        index: true,
        element: <Home />
      },
      {
        path: '/customer-signup',
        element: 
          <CreateUser
          title="Create Customer"
          description={`
            A customer can browse products, add them to the cart, and place orders.
            They can also view their order history and manage their account information.

            A user can't add, update, or delete product information, categories, or payment intents.
          `}
          endpoint="register_customer/"
        />
      },

      {
        path: '/shop-staff-signup',
        element: <CreateUser
          title="Create Shop Staff Member"
          description={`
            A member of the staff can manage (all CRUD ops) products and categories, can update the order status, 
            view and manage everyone's orders, add allowed payment methods, and more.
          `}
          endpoint="register_staff/"
        />
      },

      {
        path: '/list-users',
        element: <ListAllUsers />
      },

      {
        path: '/login',
        element: <Login />
      },

      {
        path: "/logout",
        element: <ProtectedRoute />,
        children: [
          {
            path: "",
            element: <Logout />
          }
        ]
      }
    ],
  },
]);


createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <RouterProvider router={router} />
        </ThemeProvider>
      </AuthProvider>
  </StrictMode>,
);
