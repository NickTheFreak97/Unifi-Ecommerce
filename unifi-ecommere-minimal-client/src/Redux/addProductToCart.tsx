import React from 'react';
import { createAsyncThunk } from "@reduxjs/toolkit";
import { http } from '../API/axiosHTTP';
import { getAccessToken } from '../context/AuthContext';
import { type RootState } from './store';

interface AddProductPayload {
    barcode: string;
    quantity: number;
}


export const addProductToCart = createAsyncThunk(
    'cart/addProduct',
    async (product: AddProductPayload, { rejectWithValue, getState }) => {
        const accessToken = getAccessToken()
        const cartState = getState() as RootState

        try {
            if (cartState.cart.length <= 0) {
                // TODO: Cart needs to be created 
            }

            const response = await http.post(
                '/cart/add/', 
                product, 
                {
                    headers: {
                        Authorization: ( !!accessToken ) ? `Bearer ${getAccessToken()}` : undefined
                    }
                }
            );

            return {
                "barcode": product.barcode,
                "quantity": response.status === 200 ? 0 : product.quantity
            }
        } catch (error) {
            return rejectWithValue(error.response.data);
        }
    }
);
