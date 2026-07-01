import React, { useState } from 'react'
import { Alert, Button, Box, Stack, TextField, Chip } from '@mui/material'
import JsonView from '@uiw/react-json-view'
import { lightTheme } from '@uiw/react-json-view/light';
import { http } from '../../API/axiosHTTP';
import { useAuth, setAccessToken } from '../../context/AuthContext';

interface IncompleteRequestError {
    error: string;
    username: string | null;
    email: string | null;
    password: string | null;
}

const responseToIncompleteRequest: IncompleteRequestError = {
    error: "...",
    username: "...",
    email: "...",
    password: "..."
}

interface CreateUserProps {
    title: string;
    description: string;
    endpoint: string
}

interface User {
    username: string,
    email: string,
    password: string,
}

const CreateUser: React.FC<CreateUserProps> = ({ title, description, endpoint }) => {
    const auth = useAuth();

    const [formData, setFormData ] = useState<User>({
        username: '',
        email: '',
        password: ''
    });

    const handleChange = (field: string) => (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormData((prev) => ({ ...prev, [field]: event.target.value }));
    };

    const onSubmitAction = (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();

        http.post(`/users/${endpoint}`, formData)
            .then(success => {
                if (!!success.data.access) {
                    setAccessToken(success.data.access)
                    auth.fetchUser()
                }
            })
            .catch(error => {
                console.error('error', error.response.data)
            })
    };


    return (
        <main>
            <Stack sx={{
                alignItems: 'flex-start'
            }} direction='column'>
                <h1>{ title }</h1>
                <Chip label="POST" color="post" variant='outlined'/>
            </Stack>
            <section>
                <h2>Introduction</h2>
                <h3>Use this endpoint to create a new user with customer role.</h3>
                <p>
                   { description }
                </p>

                <Alert variant="outlined" severity="info" sx={{
                    padding: 2,
                    margin: 2
                }}>
                    This endpoint does not require authentication.
                </Alert>
            </section>
            
            <section>
                <h2>
                    Request Format
                </h2>
                <JsonView value={{
                    email: "...",
                    password: "...",
                    username: "...",
                }} style={lightTheme}/>
            </section>

            <section>
                <h2>Exceptions</h2>
                <section>
                    <h3>Response To Incomplete Request</h3>
                    <p>
                        When either <code>email</code>, <code>password</code> or <code>username</code> are missing, 
                        the server will respond with a 400 status code and a JSON object indicating which fields are missing.
                        You can inspect the response data to infer what's missing.
                    </p>
                    <JsonView value={responseToIncompleteRequest} style={lightTheme}/>
                </section>

                <section>
                    <h3>Response To Blank fields</h3>
                    <p>
                        When either <code>email</code>, <code>password</code> or <code>username</code> are blank (<code>''</code>), 
                        the server will respond with a 400 status code and a JSON object indicating which fields are blank.
                        You can inspect the response data to infer what's blank.
                    </p>
                    <JsonView value={responseToIncompleteRequest} style={lightTheme}/>
                </section>

                <section>
                    <h3>Response To Duplicate User</h3>
                    <p>
                        When a user with the same <code>email</code> or <code>username</code> already exists, 
                        the server will respond with a 409 status code and a JSON object indicating the conflict.
                    </p>
                    <JsonView value={{
                        error: "..."
                    }} style={lightTheme}/>
                </section>
            </section>

            <section>
                <h3>
                    Happy Path
                </h3>
                <p>
                    When all the required fields are provided, and the user did not exist yet, the server will respond
                    with a 201 status code and a JSON object containing the newly created user's information. 

                    Since I'm using JWT for authentication, the server will also respond with a JWT access token in the response body.
                    A refresh token will be issued as an httpOnly cookie, which can be used to obtain a new access token when the current one expires.
                </p>
                <JsonView value={{
                    'success': '...',
                    'id': '...',
                    "access": '...',

                }} style={lightTheme}/>
            </section>
            
            <Box component="form" onSubmit={onSubmitAction} noValidate sx={{marginTop: 2, marginBottom: 2}}>
                <Stack spacing={2}>
                    <TextField
                        label="Name"
                        value={formData.username}
                        onChange={handleChange('username')}
                        fullWidth
                        required
                        />
        
                    <TextField
                        label="Email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange('email')}
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
                        Sign up
                    </Button>
                </Stack>
            </Box>
        </main>
    )
}


export default CreateUser;