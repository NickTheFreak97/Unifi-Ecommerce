import React, { useState, useCallback } from 'react'
import { Stack, Chip, Snackbar, Alert, type AlertColor, TextField, Box, Button } from '@mui/material'
import JsonView from '@uiw/react-json-view'
import { lightTheme } from '@uiw/react-json-view/light'
import { http } from '../API/axiosHTTP'
import { getAccessToken } from '../context/AuthContext'

interface Request {
    name: string
}

const mockInterfaceRequest: Request = {
    name: "..."
}

interface ErrorResponse {
    message: string
}

const mockErrorResponse: ErrorResponse = {
    message: "..."
}

interface HappyResponse {
   message: string
   category: string 
}

const mockHappyResponse: HappyResponse = {
    message: "...",
    category: "..."
}

const CreateCategory: React.FC = () => {
    const [categoryName, setCategoryName] = useState<string>("");
    const [isToastVisible, setIsToastVisible] = useState<boolean>(false)
    const [toastMessage, setToastMessage] = useState<string>('')
    const [toastState, setToastState] = useState<AlertColor>("info")
    
    const handleCategoryNameChange: (event: React.ChangeEvent<HTMLInputElement>) => void = useCallback((event) => {
        setCategoryName(event.target.value);
    }, []);


    const onSubmit = async (event: React.SubmitEvent<HTMLFormElement>) => {
        event.preventDefault()

        await http.post(
            '/staff/products/create_category/', 
            {
                "name": categoryName
            },
            {
                headers: {
                    Authorization: `Bearer ${getAccessToken()}`
                }
            }
        )
        .then(
            success => {
                if (!!success.data.category) {
                    setToastMessage(`Category ${success.data.category} created successfully!`)
                    setIsToastVisible(true)
                    setToastState("success")
                } else {
                    setToastMessage(`Category created successfully but response doesn't contain category name! This path should be unfeasible.`)
                    setIsToastVisible(true)
                    setToastState("error")
                }
            }
        )
        .catch(error => {
            const detail =  error.response?.data?.detail ?? error.message
            setToastMessage(`Failed to create category ${categoryName}. Status: ${error.response?.status ?? "no response"}, message: ${detail}`)
            setIsToastVisible(true)
            setToastState("error")
        })

    }

    return (
        <main>
            <Stack direction="column" sx={{ alignItems: "flex-start" }}>
                <h1>Create Category</h1>
                <Chip label="POST" color="post" variant='outlined' />
            </Stack>

            <section>
                <h2>Introduction</h2>
                <p>
                    Use this endpoint to create a new category in the system. 
                    Categories help organize products and make it easier for customers to find what they are looking for.
                    To be able to create a new category you need to be logged in as a staff member.
                </p>
            </section>

            <section>
                <h2>Request Body</h2>
                <p>The request body must contain at least a <code>name</code> key, specifying the name of the category to create.
                Since two distinct categories always have different names, this will serve as a primary key.</p>
                <JsonView value={mockInterfaceRequest} style={lightTheme} />
            </section>

            <section>
                <h2>Exceptions</h2>
                <ul>
                    <li>
                        <h3>Missing or blank name in request</h3>
                        <p>
                            In this case, the server will respond with a <code>400</code> error and a <code>message</code> in response indicating that the field must be provided.
                        </p>
                        <JsonView value={mockErrorResponse} style={lightTheme} />
                    </li>

                    <li>
                        <h3>User doesn't have permissions</h3>
                        <p>
                            In this case the server will respond with a <code>401</code> and an error <code>message</code> provifded in the response.
                        </p>
                        <JsonView value={mockErrorResponse} style={lightTheme} />
                    </li>
                    
                    <li>
                        <h3>Category already exists</h3>
                        <p>
                            In this case the server will respond with a <code>409</code> and an error <code>message</code> provifded in the response.
                        </p>
                        <JsonView value={mockErrorResponse} style={lightTheme} />
                    </li>
                </ul>
            </section>

            <section>
                <h2>Happy Path</h2>
                <p>
                    When the user is authenticated and has the correct permissions and the request is well formed, the database will create a new category with the specified name
                    and will return with a <code>201</code> response, formatted as follows:
                </p>
                <JsonView value={mockHappyResponse} style={lightTheme} />

                <Box component="form" onSubmit={onSubmit} noValidate sx={{marginTop: 2, marginBottom: 2}}>
                <Stack spacing={2}>
                    <TextField
                        label="Name"
                        value={categoryName}
                        onChange={handleCategoryNameChange}
                        fullWidth
                        required
                        />

                    <Button type="submit" variant="contained" size="large" fullWidth>
                        Create new category
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

export default CreateCategory;
