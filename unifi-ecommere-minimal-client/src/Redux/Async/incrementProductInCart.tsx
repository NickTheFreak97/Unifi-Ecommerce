import { createAsyncThunk } from "@reduxjs/toolkit";
import { http } from "../../API/axiosHTTP";
import { getAccessToken } from "../../context/AuthContext";
import axios from "axios";
import { type AddProductPayload } from "./addProductToCart";

export const incrementProductInCart = createAsyncThunk(
    'cart/increment',
    async (product: AddProductPayload, { rejectWithValue }) => {
        try {
            const accessToken = getAccessToken();
            await http.put('/cart/increment/',
                {
                    barcode: product.barcode,
                    quantity: product.quantity
                },
                {
                    headers: {
                        Authorization: !!accessToken ? `Bearer ${accessToken}` : undefined
                    },
                    withCredentials: true
                }
            );

            return {
                barcode: product.barcode,
                quantity: product.quantity
            };
        } catch (err) {
            if (axios.isAxiosError(err) && err.response) {
                if (err.response.status == 404) {
                    return {
                        barcode: product.barcode,
                        quantity: 0
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
