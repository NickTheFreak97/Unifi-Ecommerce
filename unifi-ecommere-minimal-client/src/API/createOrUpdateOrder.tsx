
import { http } from './axiosHTTP'

export interface OrderDetailProps {
    email: string,
    street: string,
    zipcode: string,
    municipality: string,
    country: string,
    currency: string
}

export const createOrUpdateOrder = async (
    order: OrderDetailProps,
    accessToken: string | null | undefined
) : Promise<boolean> => {

    return new Promise(() => {
        return http.post(
            '/order/create_or_update/',
            {
                'email': order.email,
                'shipping_street': order.street,
                'shipping_zipcode': order.zipcode,
                'shipping_municipality': order.municipality,
                'shipping_country': order.country,
                'currency': order.currency
            },
            {
                headers: {
                    'Authorization': (!!accessToken) ? `Bearer ${accessToken}` : undefined
                },
                withCredentials: true
            }
        )
        .then(() => {
            return true
        })
        .catch(error => {
            console.error(error)
            return false
        })
    })
}
