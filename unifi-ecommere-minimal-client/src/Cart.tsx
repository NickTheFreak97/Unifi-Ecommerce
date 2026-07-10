import React, { useState, useCallback, useEffect, useRef } from 'react'
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { Button } from '@mui/material';
import { useSelector } from 'react-redux'
import { fetchCart } from './Redux/fetchCart'
import { type RootState } from './Redux/store'
import { useAppDispatch } from './Redux/hooks'
import { type Category } from './routes/Catalog'
import { http } from './API/axiosHTTP'
import NumberField from './utils/NumberField';
import { addProductToCart } from './Redux/addProductToCart';
import { incrementProductInCart } from './Redux/incrementProductInCart';
import { useAuth } from './context/AuthContext';

interface ProductEntry {
    id: string;
    barcode: string;
    name: string;
    unit_price: number;
    stock: number;
    quantity: number;
    inCart: boolean;
}

interface CartProps {
    didLoad: boolean;
    error: any
}

const staticColumns: GridColDef<ProductEntry>[] = [
    {
        field: "barcode",
        headerName: "Barcode",
        flex: 2,
        minWidth: 180,
    },
    {
        field: "name",
        headerName: "Name",
        flex: 3,
        minWidth: 250,
    },
    {
        field: "unit_price",
        headerName: "Unit Price",
        type: "number",
        flex: 1,
        minWidth: 120,
        valueFormatter: value => `€${Number(value).toFixed(2)}`,
    },
    {
        field: "stock",
        headerName: "Stock",
        type: "number",
        flex: 1,
        minWidth: 100,
    },
];

const Cart: React.FC = () => {
    const cart = useSelector((state: RootState) => state.cart.items)
    const [catalog, setCatalog] = useState<Category[]>([])
    const [quantities, setQuantities] = useState<Record<string, number>>({})
    const reduxDispatch = useAppDispatch()
    const didLoad = useSelector((state: RootState) => state.cart.didLoad)
    const didFetch = useRef(false)
    const authService = useAuth()


    const handleQuantityChange = useCallback((barcode: string, value: number | null) => {
        setQuantities(prev => ({
            ...prev,
            [barcode]: value ?? 0
        }))
    }, [])

    const handleAdd = useCallback(async (product: ProductEntry) => {
        const quantity = quantities[product.barcode]

        if (quantity) {
            reduxDispatch(
                addProductToCart({
                    "barcode": product.barcode,
                    "quantity": quantity
                })
            )
        } else {
            console.warn(`Attempted to add product ${product.barcode} - ${product.name} but associated ordered quantity is 0 | undefined | null`)
        }
    }, [quantities, reduxDispatch])

    
    const handleIncrementQuantity = useCallback((product: ProductEntry) => {
        reduxDispatch(
            incrementProductInCart({
                "barcode": product.barcode,
                "quantity": 1
            })
        )
    }, [reduxDispatch])

    const fetchCatalog = useCallback(async () => {
        await http.get('/staff/products/fetch_catalog/')
            .then(response => {
                setCatalog(response.data.catalog)
            })
            .catch(
                error => {
                    console.error(error)
                }
            )
    }, [setCatalog])

    useEffect(() => {
        fetchCatalog()
    }, [])

    useEffect(() => {
        if (authService.isInitialized) {
            if (!didLoad && !didFetch.current) {
                didFetch.current = true
                reduxDispatch(fetchCart())
            }
        }
    }, [authService.isInitialized])


    const columns: GridColDef<ProductEntry>[] = [
        ...staticColumns,
        {
            field: "quantity",
            headerName: "Quantity",
            flex: 1,
            minWidth: 160,
            sortable: false,
            filterable: false,
            renderCell: (params) => (
                <NumberField
                    value={quantities[params.row.barcode] ?? 0}
                    onValueChange={(value) => handleQuantityChange(params.row.barcode, value)}
                    min={0}
                    helperText={null}
                    size="small"
                    disabled={params.row.inCart}
                />
            ),
        },
        {
            field: "actions",
            headerName: "",
            flex: 0.8,
            minWidth: 100,
            sortable: false,
            filterable: false,
            renderCell: (params) => (
                <Button
                    variant="contained"
                    size="small"
                    disabled={params.row.inCart || !quantities[params.row.barcode]}
                    onClick={() => handleAdd(params.row)}
                >
                    Add
                </Button>
            ),
        },
    ]


    return (
        <main>
            {
                (catalog.length > 0) &&
                catalog.map(
                    category => {
                        let products_for_this_category = category.products.map(
                            product => {
                                return {
                                    id: product.barcode,
                                    barcode: product.barcode,
                                    name: product.name,
                                    stock: product["product_variants"][0].stock,
                                    unit_price: product["product_variants"][0].unit_price,
                                    quantity: cart.find(item => item.barcode === product.barcode)?.quantity ?? 0,
                                    inCart: cart.some(item => item.barcode === product.barcode),
                                }
                            }
                        )

                        return (
                            <React.Fragment key={category.name}>
                                <h2>{ category.name } </h2>
                                <DataGrid
                                    key={category.name}
                                    rows={products_for_this_category}
                                    columns={columns}
                                    getRowClassName={(params) => params.row.inCart ? 'row--in-cart' : ''}
                                    sx={{
                                        '& .row--in-cart': {
                                            opacity: 0.5,
                                            pointerEvents: 'none',
                                        },
                                    }}
                                    initialState={{
                                        pagination: {
                                            paginationModel: {
                                                pageSize: 5,
                                            },
                                        },
                                    }}
                                    pageSizeOptions={[5]}
                                />
                            </React.Fragment>
                        )
                    }
                )
            }
        </main>
    )
}

export default Cart;