import React, { useState } from 'react'
import { Button, Stack, Chip } from '@mui/material'
import { http } from '../API/axiosHTTP'
import JsonView from '@uiw/react-json-view'
import { lightTheme } from '@uiw/react-json-view/light'

interface ListedUser {
    id: string
    username: string
}

interface UsersListForPermission {
    [key: string]: ListedUser[]
}

interface ListAllUsersResponse {
    users_grouped_by_group: UsersListForPermission
}

const mockList: ListAllUsersResponse = {
    "users_grouped_by_group": {
        "customer": [
            { id: "1", username: "customer1" },
            { id: "2", username: "customer2" }
        ],

        "staff": [
            { id: "3", username: "staff1" },
            { id: "4", username: "staff2" }
        ]
    }
}

const ListAllUsers: React.FC = ( ) => {
    const [roleUsersMap, setRoleUsersMap] = useState<UsersListForPermission | null>(null)

    const fetchAllUsers = async () => {
        await http.get('users/list_users_by_group/')
        .then((response) => {   
            setRoleUsersMap(response.data.users_grouped_by_group)
        })
        .catch((error) => {
            console.error(error.response.detail)
        })
    }

    return (
        <main>
            <Stack direction="column" sx={{
                alignItems: "flex-start"
            }}>
                <h1>List all users by their role</h1>
                <Chip label="GET" color="get" variant='outlined' />
            </Stack>
            <section>
                <h2>Introduction</h2>
                <p>
                    Use this endpoint to browse the list of all the available users in the system, 
                    grouped by their role.
                </p>
            </section>

            <section>
                <h2>Prerequisites</h2>
                <p>Currently everyone can hit this endpoint. Request body is not used and 
                    no authentication is required.
                </p>
            </section>

            <section>
                <h2>Response Format</h2>
                <p>The response will be a JSON object containing a dictionary. 
                    The keys will be the user roles, and the values will be arrays of users info for each role.</p>

                <JsonView value={mockList} style={lightTheme} />
            </section>

            <section>
                <h2>Call To Action</h2>

                {
                    !! roleUsersMap &&
                    <ul>
                        {
                            Object.keys(roleUsersMap).toSorted().map( role => {
                                const usersList = roleUsersMap[role]
                            
                                if (!!usersList) {
                                    return (
                                        <li key={role}>
                                            { role }
                                            <ul>
                                                {
                                                    usersList.map(user => {
                                                        return (<li key={user.id}>
                                                            <Stack direction="row" sx={{
                                                                justifyContent: "stretch",
                                                                alignItems: "center",
                                                                gap: "16px"
                                                            }}>
                                                                <strong>{user.id}</strong>
                                                                <pre>{user.username}</pre>
                                                            </Stack>
                                                        </li>)
                                                    })
                                                }
                                            </ul>
                                        </li>
                                    )
                                } else {
                                    return null
                                }
                            })
                        }
                    </ul>
                }
                
                <Button variant="contained" onClick={fetchAllUsers} fullWidth>Fetch Users</Button>
            </section>
        </main>
    )
}

export default ListAllUsers