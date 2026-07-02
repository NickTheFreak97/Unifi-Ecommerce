import { createContext, useContext, useEffect, useState, useCallback, type ReactNode } from "react";
import { http } from "../API/axiosHTTP";

interface User {
    id: number;
    email: string;
    username: string;
}

let accessToken: string | null = null;
export const setAccessToken = (token: string | null) => {
    accessToken = token;

    if (token) {
        localStorage.setItem("access_token", token);
    } else {
        localStorage.removeItem("access_token");
    }
};
export const getAccessToken = () => accessToken;

interface AuthenticatedUserInfo {
    user: User | null;
    isLoading: boolean;
    isAuthenticated: boolean;
    login: (username: string | null, password: string | null, onSuccess: ((user: User) => void) | null, onFail: ((error: any) => void) | null) => Promise<void>;
    fetchUser: () => Promise<void>;
    logout: () => Promise<void>;
}

const AuthContext = createContext<AuthenticatedUserInfo | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        setIsLoading(true)
        const storedAccessToken = localStorage.getItem('access_token')

        if (!!storedAccessToken) {
            if (!!accessToken && accessToken != storedAccessToken) {
                accessToken = null
                localStorage.removeItem('access_token')
            } else {
                if (!accessToken) {
                    accessToken = storedAccessToken
                }
            }
        }

        http.post(`/users/auth/token/refresh/`, undefined, {
            timeout: 5000,
            headers: {
                Authorization: (!!accessToken) ? `Bearer ${getAccessToken()}` : undefined 
            }
        })
            .then(response => {
                let access_token = response.data.access

                if (!!access_token) {
                    setAccessToken(access_token)
                } else {
                    console.warn("Client expected `access` on successful response but response['access'] is not set.")
                }

                return http.get(`/users/auth/who_am_i/`, {
                    headers: {
                        Authorization: `Bearer ${getAccessToken()}`
                    }
                })
            })
            .then(response => {
                setUser({
                    id: response.data.id,
                    email: response.data.email,
                    username: response.data.username
                })
            })
            .catch(error => {
                console.error(`Refresh failed with status ${error.response?.status}, message: ${error.response?.data?.error}`)
                setAccessToken(null)
            })
            .finally(() => {
                setIsLoading(false)
            })
    }, [])


    const login = useCallback(async (username: string | null, password: string | null, onSuccess: ((user: User) => void) | null, onFail: ((error: any) => void) | null) => {
        setIsLoading(true)
        try {
            const loginResponse = await http.post("/users/auth/login/", { username, password })

            if (!loginResponse.data.access) {
                console.warn("Client expected `access` on successful response but it was not set.")
                setAccessToken(null)
            } else {
                setAccessToken(loginResponse.data.access)

                const whoAmI = await http.get("/users/auth/who_am_i/", {
                    headers: { Authorization: `Bearer ${loginResponse.data.access}` }
                })

                const { id, email, username: username } = whoAmI.data

                if (!!id && !!email && !!username) {
                    setUser(
                        { id, email, username: username }
                    )

                    if (!!onSuccess) {
                        onSuccess({ id, email, username: username })
                    }
                } else {
                    console.warn("Incomplete who_am_i")
                }
            }

        } catch (error: any) {
            console.log(`Unable to perform login: ${error.response?.status ?? error.message}`)
            setAccessToken(null)

            if (!!onFail) {
                onFail(error)
            }
        } finally {
            setIsLoading(false)
        }
    }, []);



    const fetchUser = useCallback(async () => {
        if (!!accessToken) {
            setIsLoading(true)
            await http.get("/users/auth/who_am_i/", {
                headers: {
                    Authorization: `Bearer ${getAccessToken()}`,
                },
            })
            .then(
                response => {
                    setUser({
                        id: response.data.id,
                        email: response.data.email,
                        username: response.data.username,
                    });
                }
            )
            .catch(
                error => console.error(error)
            )
            .finally(() => setIsLoading(false))
        } else {
            console.warn("Attempted to fetch user data from an unauthenticated state")
        }

        
    }, []);

    const logout = useCallback(async () => {
        setIsLoading(true)
        await http.post("/users/auth/logout/", undefined, {
            headers: {
                Authorization: `Bearer ${getAccessToken()}`
            }
        })
        .finally(() => setIsLoading(false))

        setAccessToken(null);
        setUser(null);
    }, []);

    return (
        <AuthContext.Provider value={{ user, isAuthenticated: !!user, isLoading, fetchUser, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const authContext = useContext(AuthContext);
    if (!authContext) {
        throw new Error("Use `useAuth` inside an `AuthContext` to prevent this error.")
    } else {
        return authContext
    }
}