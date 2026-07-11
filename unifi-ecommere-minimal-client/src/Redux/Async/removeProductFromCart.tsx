import React from 'react';
import { createAsyncThunk } from "@reduxjs/toolkit";
import { http } from '../../API/axiosHTTP';
import { getAccessToken } from '../../context/AuthContext';

export interface RemoveProductPayload {
    barcode: string
}

export const removeProductFromCart = createAsyncThunk(
    'cart/removeProduct',
    async (product: RemoveProductPayload, { rejectWithValue }) => {
        const accessToken = getAccessToken()

        try {
            await http.delete('/cart/remove/', {
                data: {
                    barcode: product.barcode,
                },
                headers: {
                    Authorization: accessToken ? `Bearer ${accessToken}` : undefined,
                },
                withCredentials: true,
            });

            return {
                barcode: product.barcode
            };
        } catch (error: any) {
            return rejectWithValue(error.response?.data);
        }
    }
);
