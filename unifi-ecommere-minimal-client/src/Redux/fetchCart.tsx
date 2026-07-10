import { createAsyncThunk } from "@reduxjs/toolkit";
import { http } from "../API/axiosHTTP";
import { getAccessToken } from "../context/AuthContext";
import axios from "axios";
import type { RootState } from "./store";

export const fetchCart = createAsyncThunk(
    'cart/fetch',
    async (_, { rejectWithValue, getState }) => {
        try {
            const cartState = getState() as RootState

            console.warn(cartState.cart.length)
            const accessToken = getAccessToken();
            const response = await http.get('/cart/fetch/', {
                headers: {
                    Authorization: !!accessToken ? `Bearer ${accessToken}` : undefined
                }
            });
            return response.data;
        } catch (err) {
            if (axios.isAxiosError(err) && err.response) {
                if (err.response.status == 404) {
                    return {
                        cart: []
                    }
                } else {
                    return rejectWithValue(err.response.data)
                }
            } else {
                throw err
            }
        }
    }
);
