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

import CreateUser from "./routes/Signup/CreateUser";
import { http } from "./API/axiosHTTP";

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
          onSubmit={(event, data) => {
            event.preventDefault();
            http.post('/users/register_customer/', data)
              .then(success => {
                  console.log('success', success.data)
              })
              .catch(error => {
                console.error('error', error.response.data)
              })
          }}
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
          onSubmit={() => {}}
        />
      }
    ],
  },
]);

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

console.log(import.meta.env);
console.log('MODE:', import.meta.env.MODE);


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
