import React from 'react';
import { createAsyncThunk } from "@reduxjs/toolkit";
import { http } from '../API/axiosHTTP';
import { getAccessToken } from '../context/AuthContext';
import { type RootState } from './store';

export interface AddProductPayload {
    barcode: string;
    amount: number;
}


export const addProductToCart = createAsyncThunk(
    'cart/addProduct',
    async (product: AddProductPayload, { rejectWithValue, getState }) => {
        const accessToken = getAccessToken()
        const cartState = getState() as RootState

        try {
            if (cartState.cart.items.length <= 0) {
                const cartCreationResponse = await http.post('/cart/create/',
                    { 'cart': [ product ] },
                    {
                        headers: {
                            Authorization: accessToken ? `Bearer ${accessToken}` : undefined
                        }
                    }
                );

                console.log(`Cart ${cartCreationResponse.data.status == 200 ? "existed" : "created"}`)
                return {
                    barcode: product.barcode,
                    quantity: product.amount
                }
            } else {
                const response = await http.put(
                    '/cart/add/',
                    {
                        "barcode": product.barcode,
                        "quantity": product.amount
                    },
                    {
                        headers: {
                            Authorization: accessToken ? `Bearer ${accessToken}` : undefined
                        }
                    }
                );

                return {
                    barcode: product.barcode,
                    quantity: response.status === 200 ? 0 : product.amount
                };
            }
        } catch (error: any) {
            return rejectWithValue(error.response?.data);
        }
    }
);
