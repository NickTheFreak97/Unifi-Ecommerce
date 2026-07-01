import axios from 'axios'

export const http = axios.create({
    baseURL: `${import.meta.env.VITE_API_URL}`,
    withCredentials: true
})

/*
const { data } = await http.get("/auth/who_am_i/", {
  headers: { Authorization: `Bearer ${getAccessToken()}` },
});

This is how to makle an authenticated request that uses access token
*/