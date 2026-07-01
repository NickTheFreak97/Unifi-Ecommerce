import "@mui/material/styles";

interface CustomColor {
  main: string;
  light?: string;
  dark?: string;
  contrastText?: string;
}

declare module "@mui/material/styles" {
  interface Palette {
    get: CustomColor;
    post: CustomColor;
    put: CustomColor;
    patch: CustomColor;
    delete: CustomColor;
  }

  interface PaletteOptions {
    get?: CustomColor;
    post?: CustomColor;
    put?: CustomColor;
    patch?: CustomColor;
    delete?: CustomColor;
  }
}

declare module "@mui/material/Chip" {
  interface ChipPropsColorOverrides {
    get: true;
    post: true;
    put: true;
    patch: true;
    delete: true;
  }
}