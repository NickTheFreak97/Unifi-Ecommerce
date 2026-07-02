import React, { useState } from "react";
import { Box, Stack, Button, TextField, Snackbar, Alert, type AlertColor, Chip } from '@mui/material'
import { useAuth } from "../context/AuthContext";
import JsonView from "@uiw/react-json-view";
import { lightTheme } from '@uiw/react-json-view/light';


interface LoginData {
    username: string | null;
    password: string | null;
}

const mockLoginData: LoginData = {
    username: "...",
    password: "..."
}


interface ResponseToIncompleteRequest {
    error: string
}

const mockResponseToIncompleteRequest: ResponseToIncompleteRequest = {
    error: "..."
}

interface ResponseToAuthSuccess {
    user: string,
    access: string
}

const mockSuccessResponse: ResponseToAuthSuccess = {
    user: "...",
    access: "..."
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
            <Stack direction="column" sx={{
                alignItems: "flex-start"
            }}>
                <h1>Log in</h1>
                <Chip variant="outlined" color="post" label="POST"/>
            </Stack>

            <section>
                <h2>Introduction</h2>
                <h3>Use this endpoint to log in an existing user, irregardless of their group.</h3>
                <p>
                    When an user is successfully logged in, the Django backend provides an access token in the response body under a <code>access</code> key, 
                    and issues an HTTPOnly cookie with a refresh token that can be used to acquire a new access token when the previous one expires.
                </p>
            </section>

            <section>
                <h2>Request format</h2>
                <p>
                    The request must contain a <code>username</code> and a <code>password</code> field.
                </p>

                <JsonView value={mockLoginData} style={lightTheme}/>
            </section>

            <section>
                <h2>Exceptions</h2>
                <ul>
                    <li>
                        <h3>Response to Incomplete request</h3>
                        <p>When either <code>username</code> or <code>password</code> are not provided, the server responds with an error <code>400</code> and the response is structured like this:</p>
                        <JsonView value={mockResponseToIncompleteRequest} style={lightTheme} />
                    </li>
                    <li>
                        <h3>Response to Invalid Credentials</h3>
                        <p>When the provided credentials do not match any existing user, the server responds with an error with status <code>401</code> and the following structure:</p>
                        <JsonView value={mockResponseToIncompleteRequest} style={lightTheme} />
                    </li>
                </ul>
            </section>

            <section>
                <h2>Happy Path</h2>
                <p>
                    When both the credentials are provided and match a user on the database, the server authenticates the user in the sense of <code>django.contrib.auth</code> and issues a refresh token for the matched user.
                    The server also sets an HTTPOnly cookie that is expected to be attached to every request where <code>permission_classes = [IsAuthenticated]</code>, and can be used to claim a new access token when the existing one expires.
                    Protected endopoints will expect an header containing <code>Authorization: Bearer &#123;access_token&#125;</code>. Response will have status <code>200</code>.
                </p>
                <JsonView value={mockSuccessResponse} style={lightTheme}/>
            </section>

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