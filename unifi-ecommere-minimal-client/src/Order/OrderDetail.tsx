import React, { useState, useCallback } from 'react'
import { Button, Box, MenuItem, InputLabel, Stack, Select, TextField, FormGroup } from '@mui/material'
import { getAccessToken } from '../context/AuthContext'
import { http } from '../API/axiosHTTP'

interface OrderDetailPageProps {
    onSubmit: (
        event: React.SubmitEvent<HTMLFormElement>,
        formData: OrderDetailProps
    ) => void
}

export interface OrderDetailProps {
    email: string,
    street: string,
    zipcode: string,
    municipality: string,
    country: string,
    currency: string
}



const OrderDetail: React.FC<OrderDetailPageProps> = ({ onSubmit }) => {
    const [formData, setFormData] = useState<OrderDetailProps>({
        email: '',
        street: '',
        zipcode: '',
        municipality: '',
        country: '',
        currency: ''
    });

    const createOrUpdateorder = useCallback(async (order: OrderDetailProps, onSuccess?: (response: any) => void) => {
        const accessToken = getAccessToken()

        await http.post(
        '/orders/create_or_update/',
        {
            'email': order.email,
            'street': order.street,
            'zipcode': order.zipcode,
            'municipality': order.municipality,
            'country': order.country,
            'currency': order.currency
        },
        {
            headers: {
                'Authorization': (!!accessToken) ? `Bearer ${accessToken}` : undefined
            },
            withCredentials: true
        }
    )
        .then(response => {
            if (!!onSuccess) {
                onSuccess(response.data)
            }
        })
        .catch(error => {
            console.error(error)
        })
    }, [])

  return (
    <section>
        <h2>Order Details</h2>
        <Box component="form" noValidate sx={{
            margin: 2
        }} 
        onSubmit={(event: React.SubmitEvent<HTMLFormElement>) => {
            event.preventDefault();

            createOrUpdateorder(formData, (response) => {
                console.warn(response)
                onSubmit(event, formData);  
            })
        }}>
            <Stack sx={{
                display: 'flex',
                flexDirection: 'column',
                gap: 3
            }}>
                <TextField
                    label="Email"
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={(changeEvent) => {
                        setFormData(
                            (prev: OrderDetailProps) => ({ ...prev, email: changeEvent.target.value })
                        )
                    }}
                    fullWidth
                    required
                    autoComplete="email"
                    />
                
                <FormGroup>
                    <InputLabel id="unit-price-currency">Currency</InputLabel>
                    <Select
                        labelId="unit-price-currency"
                        id="unit-price-currency-select"
                        value={formData.currency}
                        label="Currency"
                        onChange={(changeEvent) => {
                            setFormData(
                                (prev: OrderDetailProps) => ({ ...prev, currency: changeEvent.target.value })
                            )
                        }}
                        fullWidth
                    >
                        <MenuItem value="EUR">EUR</MenuItem>
                    </Select>
                </FormGroup>

                <FormGroup>
                    <InputLabel id="country-select">Country</InputLabel>
                    <Select
                        labelId="country-select"
                        id="country-select-select"
                        value={formData.country}
                        label="Country"
                        onChange={(changeEvent) => {
                            setFormData(
                                (prev: OrderDetailProps) => ({ ...prev, country: changeEvent.target.value })
                            )
                        }}
                        fullWidth
                    >
                        <MenuItem value="IT">Italia</MenuItem>
                    </Select>
                </FormGroup>

                <TextField
                    label="Via/Viale"
                    type="text"
                    name="address"
                    value={formData.street}
                    onChange={(changeEvent) => {
                        setFormData(
                            (prev: OrderDetailProps) => ({ ...prev, street: changeEvent.target.value })
                        )
                    }}
                    fullWidth
                    required
                    autoComplete="address-line1"
                    />

                <TextField
                    label="Provincia"
                    type="text"
                    name="municipality-2"
                    value={formData.municipality}
                    onChange={(changeEvent) => {
                        setFormData(
                            (prev: OrderDetailProps) => ({ ...prev, municipality: changeEvent.target.value })
                        )
                    }}
                    fullWidth
                    required
                    autoComplete="municipality-2"
                    />


                <TextField
                    label="CAP"
                    type="text"
                    name="zipcode"
                    value={formData.zipcode}
                    onChange={(changeEvent) => {
                        setFormData(
                            (prev: OrderDetailProps) => ({ ...prev, zipcode: changeEvent.target.value })
                        )
                    }}
                    fullWidth
                    required
                    autoComplete="zipcode"
                    />

                <Button
                    variant="contained"
                    color="primary"
                    type="submit"
                >
                    Submit
                </Button>
            </Stack>
        </Box>
    </section>
  )
}

export default OrderDetail;

