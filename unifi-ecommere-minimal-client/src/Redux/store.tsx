import { configureStore } from "@reduxjs/toolkit";
import cartReducer from "./Reducers/cartReducer";

const store = configureStore({
    reducer: {
        cart: cartReducer
    }
});

export { store };

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;