import React, { useState, useCallback, useEffect } from 'react'
import { DataGrid, type GridColDef } from '@mui/x-data-grid';
import { useSelector } from 'react-redux'
import { fetchCart } from './Redux/fetchCart'
import { type RootState } from './Redux/store'
import { useAppDispatch } from './Redux/hooks'
import { type Category } from './routes/Catalog'
import { http } from './API/axiosHTTP'
import NumberField from './utils/NumberField';
import { Button } from '@mui/material';
import { getAccessToken } from './context/AuthContext';

interface ProductEntry {
    id: string;
    barcode: string;
    name: string;
    unit_price: number;
    stock: number;
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

    const cart = useSelector((state: RootState) => state.cart)
    const [catalog, setCatalog] = useState<Category[]>([])
    const [quantities, setQuantities] = useState<Record<string, number>>({})
    const reduxDispatch = useAppDispatch()

    const handleQuantityChange = useCallback((productId: string, value: number | null) => {
        setQuantities(prev => ({
            ...prev,
            [productId]: value ?? 0
        }))
    }, [])

    const handleAdd = useCallback(async (product: ProductEntry) => {
        // TODO: Handle tap on add to cart
    }, [quantities, reduxDispatch])

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
                    value={quantities[params.row.id] ?? 0}
                    onValueChange={(value) => handleQuantityChange(params.row.id, value)}
                    min={0}
                    helperText={null}
                    size="small"
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
                    disabled={false}
                    onClick={() => handleAdd(params.row)}
                >
                    Add
                </Button>
            ),
        },
    ]

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
        reduxDispatch(fetchCart())
    }, [])


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
                                    unit_price: product["product_variants"][0].unit_price
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
            <Button 
            onClick={async () => {
                await http.post('/cart/create/', null, {
                    headers: {
                        Authorization: `Bearer ${getAccessToken()}`
                    }
                })
                .then(
                    (response) => {
                        console.log(response.data)
                    }
                )
                .catch(
                    error => {
                        console.error(error)
                    }
                )
            }}
            variant='contained' fullWidth>
                Action
            </Button>
        </main>
    )
}

export default Cart;