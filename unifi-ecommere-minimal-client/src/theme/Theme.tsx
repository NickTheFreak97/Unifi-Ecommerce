import { createTheme } from "@mui/material/styles";
import "@mui/material/styles";


const theme = createTheme({
  palette: {
    mode: 'dark',

    get: {
      main: "#4CAF50",
      contrastText: "#fff",
    },
    post: {
      main: "#FF9800",
      contrastText: "#000",
    },
    put: {
      main: "#2196F3",
      contrastText: "#fff",
    },
    patch: {
      main: "#9C27B0",
      contrastText: "#fff",
    },
    delete: {
      main: "#F44336",
      contrastText: "#fff",
    },
  },
});

export default theme;