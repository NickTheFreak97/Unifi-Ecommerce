import React, { useState } from 'react'
import { Button, Stack, Chip, Snackbar, Alert, type AlertColor } from '@mui/material'
import { useAuth } from '../../context/AuthContext'

const Logout: React.FC = () => {

    const authService = useAuth();
    const [isToastVisible, setIsToastVisible] = useState<boolean>(false)
    const [toastSeverity, setToastSeverity] = useState<AlertColor>("info")
    const [toastMessage, setToastMessage] = useState<string>('')

    const onLogout = (event: React.MouseEvent<HTMLButtonElement>) => {
        event.preventDefault()

        authService.logout(
            () => {
                setToastMessage("User successfully logged out")
                setToastSeverity("success")
                setIsToastVisible(true)
            },

            (error) => {
                setToastMessage(`Unable to logout user: ${error.response?.data?.detail ?? error.message}. Status ${error.response?.status ?? "n/a"}`)
                setToastSeverity("error")
                setIsToastVisible(true)
            }
        )
    }

    return (
        <main>
            <Stack direction="column" sx={{
                alignItems: 'flex-start'
            }}>
                <h1>Logout current user</h1>
                <Chip label="POST" variant='outlined' color="post" />
            </Stack>

            <section>
                <h2>Introduction</h2>
                <p>
                    This endpoint is used by authenticated users to revoke access to protected routes referred to as `logout`. 
                </p>
            </section>

            <section>
                <h2>Request</h2>
                Request body is not used. Request header must have <code>Authorization: Bearer &#123;access_token&#125;</code>, and the <code>refres_token</code> HTTPOnly cookie is extracted from the request.
                The token is blacklisted, the cookie is deleted, and the session is closed.
            </section>

            <section>
                <h2>Exceptions</h2>
                <ul>
                    <li>
                        <h3>
                            Blacklisted / Invalid / Missing refresh token
                        </h3>
                    </li>
                </ul>
            </section>

            <section>
                <h2>Expected client behavior</h2>
                <p>The client should clear the revoked access token from cookies/storage/store or whatever was used as a client persistance mean. It also should clear current user presentation (so that it's clear to the user that they're not logged in).</p>
            </section>

            <section>
                <h2>Call To Action</h2>
                <Button type="button" variant="contained" size="large" onClick={onLogout} fullWidth>
                    Log Out
                </Button>
                <Snackbar
                    open={isToastVisible}
                    autoHideDuration={6000}
                    anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                    onClose={() => setIsToastVisible(false)}
                >
                    <Alert severity={toastSeverity} variant="filled" sx={{ width: "100%" }}>
                        { toastMessage }
                    </Alert>
                </Snackbar>
            </section>
        </main>
    )
}

export default Logout