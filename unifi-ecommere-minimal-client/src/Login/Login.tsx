import React, { useState } from "react";
import { Box, Stack, Button, TextField, Snackbar, Alert, type AlertColor } from '@mui/material'
import { useAuth } from "../context/AuthContext";

interface LoginData {
    username: string | null;
    password: string | null;
}

const Login: React.FC = () => {
    const handleChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormData((prev: LoginData) => ({ ...prev, [field]: event.target.value }));
    };

    const [formData, setFormData ] = useState<LoginData>({
        username: '',
        password: ''
    });
    const [isToastVisible, setIsToastVisible] = useState<boolean>(false)
    const [toastMessage, setToastMessage] = useState<string>('')
    const [toastState, setToastState] = useState<AlertColor>("info")

    const authProvider = useAuth();

    const onSubmit = (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();
        
        authProvider.login(
            formData.username, 
            formData.password, 
            (user) => {
                setToastMessage(`Authenticated ${JSON.stringify(user)}`)
                setToastState("success")
                setIsToastVisible(true)
            },
            (error) => {
                setToastMessage(`Error ${error.response.status} with message ${error.response.message}`)
                setToastState("error")
                setIsToastVisible(true)
            }
        )
        console.log(`Attempted login of ${formData.username} : ${formData.password}`)
    }

    return (
        <main>
            <Box component="form" onSubmit={onSubmit} noValidate sx={{marginTop: 2, marginBottom: 2}}>
                <Stack spacing={2}>
                    <TextField
                        label="Name"
                        value={formData.username}
                        onChange={handleChange('username')}
                        fullWidth
                        required
                    />

                    <TextField
                        label="Password"
                        type="password"
                        value={formData.password}
                        onChange={handleChange('password')}
                        fullWidth
                        required
                    />
        
                    <Button type="submit" variant="contained" size="large" fullWidth>
                        Log In
                    </Button>
                </Stack>
            </Box>

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
            
        </main>
    )
}

export default Login