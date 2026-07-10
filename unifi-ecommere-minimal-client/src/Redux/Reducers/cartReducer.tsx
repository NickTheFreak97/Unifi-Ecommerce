import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { fetchCart } from '../fetchCart'
import { addProductToCart } from '../addProductToCart'

export interface CartItem {
    barcode: string
    amount: number
}

export type CartState = CartItem[]

const initialState: CartState = []

const cartSlice = createSlice({
    name: 'cart',
    initialState,
    reducers: {
        increment: (state, action: PayloadAction<{ barcode: string; amount?: number }>) => {
            const { barcode, amount = 1 } = action.payload

            const product = state.find(
                item => item.barcode === barcode
            )

            if (product) {
                product.amount += amount
            } else {
                console.error(`Product with barcode ${barcode} not found in cart.`)
            }
        },

        decrement: (state, action: PayloadAction<{ barcode: string; amount?: number }>) => {
            const { barcode, amount = 1 } = action.payload

            const productIndex = state.findIndex(
                item => item.barcode === barcode
            )

            if (productIndex === -1) {
                console.error(`Product with barcode ${barcode} not found in cart.`)
                return
            }

            const product = state[productIndex]

            if (amount >= product.amount) {
                state.splice(productIndex, 1)
            } else {
                product.amount -= amount
            }
        },

        remove: (state, action: PayloadAction<{ barcode: string }>) => {
            const index = state.findIndex(
                item => item.barcode === action.payload.barcode
            )

            if (index !== -1) {
                state.splice(index, 1)
            } else {
                console.error(
                    `Product with barcode ${action.payload.barcode} not found in cart.`
                )
            }
        },
    },

    extraReducers: (builder) => {
        builder
            .addCase(fetchCart.pending, (state, action) => {

            })
            .addCase(fetchCart.fulfilled, (state, action) => {
                
            })
            .addCase(fetchCart.rejected, (state, action) => {
                if (action.payload) {
                    // TODO: handle server structured error
                } else {
                    // TODO: handle other errors (network, etc)
                }
            });

        builder 
            .addCase(addProductToCart.pending, (state, action) => { })
            .addCase(addProductToCart.fulfilled, (state, action) => { 
                const { barcode, quantity = 1 } = action.payload

                const product = state.find(
                    item => item.barcode === barcode
                )

                if (product) {
                    product.amount += quantity
                } else {
                    state.push({ barcode, amount: quantity })
                }
            })
            .addCase(addProductToCart.rejected, (state, action) => { 
                if (action.payload) {
                    // TODO: handle server structured error
                } else {
                    // TODO: handle other errors (network, etc)
                }
            })
    }
})

export const { increment, decrement, remove } = cartSlice.actions
export default cartSlice.reducer