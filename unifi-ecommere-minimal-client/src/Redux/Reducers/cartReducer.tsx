import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { fetchCart } from '../fetchCart'

interface CartItem {
    barcode: string
    amount: number
}

interface CartState {
    items: CartItem[]
}

const initialState: CartState = {
    items: []
}

const cartSlice = createSlice({
    name: 'cart',
    initialState,
    reducers: {
        increment: (state, action: PayloadAction<{ barcode: string; amount?: number }>) => {
            const { barcode, amount = 1 } = action.payload

            const product = state.items.find(
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

            const productIndex = state.items.findIndex(
                item => item.barcode === barcode
            )

            if (productIndex === -1) {
                console.error(`Product with barcode ${barcode} not found in cart.`)
                return
            }

            const product = state.items[productIndex]

            if (amount >= product.amount) {
                state.items.splice(productIndex, 1)
            } else {
                product.amount -= amount
            }
        },

        add: (state, action: PayloadAction<{ barcode: string; amount?: number }>) => {
            const { barcode, amount = 1 } = action.payload

            const product = state.items.find(
                item => item.barcode === barcode
            )

            if (product) {
                product.amount += amount
            } else {
                state.items.push({ barcode, amount })
            }
        },

        remove: (state, action: PayloadAction<{ barcode: string }>) => {
            const index = state.items.findIndex(
                item => item.barcode === action.payload.barcode
            )

            if (index !== -1) {
                state.items.splice(index, 1)
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

            });
    }
})

export const { increment, decrement, add, remove } = cartSlice.actions
export default cartSlice.reducer