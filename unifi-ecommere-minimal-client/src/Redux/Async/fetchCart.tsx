import { createAsyncThunk } from "@reduxjs/toolkit";
import { http } from "../../API/axiosHTTP";
import { getAccessToken } from "../../context/AuthContext";
import axios from "axios";
import type { CartItem } from "../Reducers/cartReducer";

interface FetchCartResult {
    cart: [CartItem]
}

export const fetchCart = createAsyncThunk<FetchCartResult, void>(
    'cart/fetch',
    async (_, { rejectWithValue }) => {
        try {
            const accessToken = getAccessToken();

            const response = await http.get('/cart/fetch/', {
                headers: {
                    Authorization: !!accessToken ? `Bearer ${accessToken}` : undefined
                },
                withCredentials: true
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
