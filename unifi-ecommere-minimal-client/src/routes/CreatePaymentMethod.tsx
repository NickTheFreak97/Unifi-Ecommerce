import React, { useState, useCallback } from "react";
import { Chip, Box, Stack, TextField, InputLabel, FormGroup, Select, MenuItem, Button, Snackbar, Alert, type AlertColor } from '@mui/material'
import JsonView from "@uiw/react-json-view";
import { lightTheme } from "@uiw/react-json-view/light";
import { http } from "../API/axiosHTTP";
import { getAccessToken } from "../context/AuthContext";

enum PaymentMethodType {
    wallet = "wallet",
    bank = "bank",
    card = "card"
}

interface PaymentMethodCreationRequest {
    type: PaymentMethodType,
    name: string,
    provider: string
}

const mockPaymentCreationRequest: PaymentMethodCreationRequest = {
    type: PaymentMethodType.card,
    name: "visa",
    provider: "stripe"
}

const CreatePaymentMethod: React.FC = () => {

    const [formData, setFormData] = useState<PaymentMethodCreationRequest>({
        type: PaymentMethodType.card,
        name: "",
        provider: ""
    })

    const [isToastVisible, setIsToastVisible] = useState<boolean>(false)
    const [toastMessage, setToastMessage] = useState<string>('')
    const [toastState, setToastState] = useState<AlertColor>("info")

    const handleCreatePaymentMethod = useCallback(async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault()

        await http.post('/payment/create_method/', formData, {
            headers: {
                'Authorization': (!!getAccessToken()) ? `Bearer ${getAccessToken()}` : undefined
            }, 
            withCredentials: true
        })
        .then(
            success => {
                setToastState('success')
                if (success.data.status == 201) {
                    setToastMessage("Successfully created payment method")
                } else {
                    if (success.data.status == 204) {
                        setToastMessage("Payment method already existed")
                    } else {
                        setToastMessage("Successfully created payment method")
                    }
                }
                setIsToastVisible(true)
            }
        )
        .catch(error => {
            setToastState('error')
            setToastMessage(`Error creating method ${error.response?.data?.detail ?? error.response?.data.message} with status ${error.response.status}`)
        })
    }, [formData, toastMessage, isToastVisible])

    return (
        <main>
            <Stack direction="column" sx={{
                alignItems: "flex-start"
            }}>
                <h1>Create Payment Method</h1>
                <Chip label="POST" variant="outlined" color="post" />
            </Stack>

            <section>
                <h2>Request format</h2>
                <p>
                    Include a <code>name</code> representing the name of the network, and a <code>provider</code> representing the name of a PSP. Currently, <code>type</code> can be either "wallet" | "bank" | "card"
                </p>
                <JsonView value={mockPaymentCreationRequest} style={lightTheme} />
            </section>

            <section>
                <h2>
                    Exceptions
                </h2>

                <ul>
                    <li>
                        <h3>No user authentication</h3>
                        <p>The server responds with a <code>401</code> status code response.</p>
                    </li>
                    <li>
                        <h3>User doesn't have permission to write on PaymentMethod</h3>
                        <p>The server responds with a <code>403</code> status code response.</p>
                    </li>
                    <li>
                        <h3>Invalid, blank or missing parameters.</h3>
                        <p>A structured response is provided via serializer validation, returning <code>400</code> status response.</p>
                    </li>
                </ul>
            </section>

            <section>
                <Box component="form" onSubmit={handleCreatePaymentMethod} noValidate>
                    <Stack sx={{ 
                            display: 'flex', 
                            flexDirection: 'column',
                            gap: 2
                        }}>
                        <FormGroup>
                            <InputLabel id="payment-method-select">Country</InputLabel>
                            <Select
                                labelId="payment-method-select"
                                id="payment-method-select-select"
                                value={formData.type}
                                label="Country"
                                onChange={(changeEvent) => {
                                    setFormData(
                                        (prev: PaymentMethodCreationRequest) => ({ ...prev, type: changeEvent.target.value })
                                    )
                                }}
                                fullWidth
                            >
                                <MenuItem value="wallet">Wallet</MenuItem>
                                <MenuItem value="card">Card</MenuItem>
                                <MenuItem value="bank">Bank</MenuItem>
                            </Select>
                        </FormGroup>

                        <TextField
                            label="Name"
                            type="text"
                            name="name"
                            value={formData.name}
                            onChange={(changeEvent) => {
                                setFormData(
                                    (prev: PaymentMethodCreationRequest) => ({ ...prev, name: changeEvent.target.value })
                                )
                            }}
                            fullWidth
                            required
                            />

                        <TextField
                            label="Provider"
                            type="text"
                            name="name"
                            value={formData.provider}
                            onChange={(changeEvent) => {
                                setFormData(
                                    (prev: PaymentMethodCreationRequest) => ({ ...prev, provider: changeEvent.target.value })
                                )
                            }}
                            fullWidth
                            required
                            />  

                        <Button type="submit" variant="contained" fullWidth>
                            Create
                        </Button>

                        <Snackbar
                            open={isToastVisible}
                            autoHideDuration={6000}
                            anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                            onClose={() => setIsToastVisible(false)}
                        >
                            <Alert severity={toastState} variant="filled" sx={{ width: "100%" }}>
                                { toastMessage }
                            </Alert>
                        </Snackbar>

                    </Stack>

                </Box>
            </section>
        </main>
    )
}

export default CreatePaymentMethod;