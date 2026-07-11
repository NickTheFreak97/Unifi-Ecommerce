import { createSlice, type PayloadAction } from '@reduxjs/toolkit'
import { fetchCart } from '../Async/fetchCart'
import { addProductToCart } from '../Async/addProductToCart'
import { incrementProductInCart } from '../Async/incrementProductInCart'
import { decrementProductInCart } from '../Async/decrementProductInCart'

export interface CartItem {
    barcode: string
    quantity: number
}

export interface CartState {
    items: CartItem[]
    didLoad: boolean
    error: any
}

const initialState: CartState = {
    items: [],
    didLoad: false,
    error: null,
}

const cartSlice = createSlice({
    name: 'cart',
    initialState,
    reducers: {
        decrement: (state, action: PayloadAction<{ barcode: string; quantity?: number }>) => {
            const { barcode, quantity = 1 } = action.payload

            const productIndex = state.items.findIndex(
                item => item.barcode === barcode
            )

            if (productIndex === -1) {
                console.error(`Product with barcode ${barcode} not found in cart.`)
                return
            }

            const product = state.items[productIndex]

            if (quantity >= product.quantity) {
                state.items.splice(productIndex, 1)
            } else {
                product.quantity -= quantity
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
            .addCase(fetchCart.pending, (state) => {
                state.error = null
            })
            .addCase(fetchCart.fulfilled, (state, action) => {
                state.items = action.payload.cart.map(
                    item => ({
                        barcode: item.barcode,
                        quantity: item.quantity
                    })
                )
                state.didLoad = true
                state.error = null
            })
            .addCase(fetchCart.rejected, (state, action) => {
                state.didLoad = true
                state.error = action.payload ?? action.error
            });

        builder
            .addCase(addProductToCart.pending, (state) => {
                state.error = null
            })
            .addCase(addProductToCart.fulfilled, (state, action) => {
                const { barcode, quantity = 1 } = action.payload

                const product = state.items.find(
                    item => item.barcode === barcode
                )

                if (product) {
                    product.quantity += quantity
                } else {
                    state.items.push({ barcode, quantity: quantity })
                }
            })
            .addCase(addProductToCart.rejected, (state, action) => {
                state.error = action.payload ?? action.error
            })

            builder.addCase(incrementProductInCart.pending, (state) => {
                state.error = null
            })
            .addCase(incrementProductInCart.fulfilled, (state, action) => {
                 const { barcode, quantity = 1 } = action.payload

                const product = state.items.find(
                    item => item.barcode === barcode
                )

                if (product) {
                    product.quantity += quantity
                } else {
                    console.error(`Product with barcode ${barcode} not found in cart.`)
                }
            })
            .addCase(incrementProductInCart.rejected, (state, action) => {
                state.error = action.payload ?? action.error
            })

            builder.addCase(decrementProductInCart.pending, (state, action) => {
                state.error = null
            })
            .addCase(decrementProductInCart.fulfilled, (state, action) => {
                const { barcode, quantity = 1 } = action.payload

                const productIndex = state.items.findIndex(
                    item => item.barcode === barcode
                )

                if (productIndex === -1) {
                    console.error(`Product with barcode ${barcode} not found in cart.`)
                    return
                }

                const product = state.items[productIndex]

                if (quantity >= product.quantity) {
                    state.items.splice(productIndex, 1)
                } else {
                    product.quantity -= quantity
                }
            })
            .addCase(decrementProductInCart.rejected, (state, action) => {
                state.error = action.payload
            })
    }
})

export const { decrement, remove } = cartSlice.actions
export default cartSlice.reducer