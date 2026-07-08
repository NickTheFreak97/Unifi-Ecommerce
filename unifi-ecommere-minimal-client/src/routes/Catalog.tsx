import React, { useState, useCallback } from 'react'
import { Button, Box, Chip, Stack } from '@mui/material'
import { http } from '../API/axiosHTTP'
import JsonView from '@uiw/react-json-view'
import { lightTheme } from '@uiw/react-json-view/light'

export interface ProductVariant {
    barcode: string
    stock: number
    unit_price: number
}

export interface Product {
    barcode: string
    name: string,
    product_variants: ProductVariant[]
}

export interface Category {
    name: string
    products: Product[]
}

export interface Catalog {
    catalog: Category[]
}

const mockResponse: Catalog = {
    'catalog': [
        {
            name: "...",
            products: [
                {
                    barcode: '...',
                    name: '...',
                    product_variants: [
                        {
                            barcode: '...',
                            unit_price: 1.5,
                            stock: 0.0
                        }
                    ]
                }
            ]
        }
    ]
}

const Catalog: React.FC = () => {
    const [catalog, setCatalog] = useState<Category[]>([])

    const fetchCatalog = useCallback(async () => {
        await http.get('/staff/products/fetch_catalog/')
            .then(response => {
                setCatalog(response.data.catalog)
                console.log(response.data.catalog)
            })
            .catch(
                error => {
                    console.error(error)
                }
            )
    }, [setCatalog])

    return (
        <main>
            <Stack sx={{
                direction: "column",
                alignItems: "flex-start"
            }}>
                <h1>
                    List products and variants by category
                </h1>
                <Chip label="GET" color="get" variant='outlined'/>
            </Stack>

            <section>
                <h2>
                    Introduction
                </h2>
                <p>
                    Use this endpoint to tree-view all categories, and their products.
                </p>
            </section>

            <section>
                <h2>Response format</h2>
                <JsonView value={mockResponse} style={lightTheme} />
            </section>


            <section>
                <h2>Perform request</h2>
                <Box component="form" noValidate onSubmit={async (event) => {
                    event.preventDefault()
                    await fetchCatalog();
                }}
                sx={{
                    margin: 2
                }}
                >
                    <Button type="submit" variant="contained" size="large" fullWidth>
                        Fetch catalog
                    </Button>
                </Box>
            </section>
            
            {
                catalog.length > 0 &&
                    <ul>
                        {
                            catalog.map( category => {
                                return (
                                    <li key={category.name}>
                                        <h2>
                                            { category.name }
                                        </h2>
                                            <ul>
                                                {
                                                    category.products.map(
                                                        product => {
                                                            return (
                                                                <li key={product.name}>
                                                                    { `Name: ${product.name} | Barcode: ${product.barcode}` }
                                                                    <ul>
                                                                        {
                                                                            product.product_variants.map(
                                                                                variant => {
                                                                                    return (
                                                                                        <li key={variant.barcode}>
                                                                                            {`Barcode: ${variant.barcode} | Price: ${variant.unit_price} | Stock: ${variant.stock}`}
                                                                                        </li>
                                                                                    )
                                                                                }
                                                                            )
                                                                        }
                                                                    </ul>
                                                                </li>
                                                            )
                                                        }
                                                    )
                                                }
                                            </ul>
                                    </li>
                                )
                            })
                        }
                    </ul>
            }
        </main>
    )
}

export default Catalog;