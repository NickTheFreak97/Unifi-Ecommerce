import React, { useState, useRef, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { loadStripe } from "@stripe/stripe-js";
import { Elements, PaymentElement, useStripe, useElements } from "@stripe/react-stripe-js";
import { http } from "../../../API/axiosHTTP";
import { getAccessToken } from "../../../context/AuthContext";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

const StripePaymentPage: React.FC = ( ) => {
    const [clientSecret, setClientSecret] = useState("");
    const idempotencyKey = useRef(uuidv4()).current;


    useEffect(() => {
        http.post('/payment/stripe/intent/create/', {
            'idempotency_key': idempotencyKey
        }, {
            headers: {
                Authorization: (!!getAccessToken()) ? `Bearer ${getAccessToken()}` : undefined
            },
            withCredentials: true
        })
        .then(
            response => {
                console.log(response.data)
                setClientSecret(response.data.client_secret)
            }
        )
        .catch(
            error => {
                console.log(error.data)
            }
        )
       
    }, []);

    if (!clientSecret) return <p>Loading…</p>;

    return (
        <Elements stripe={stripePromise} options={{ clientSecret }}>
        <CheckoutForm />
        </Elements>
    );
}


const CheckoutForm: React.FC = () => {
    const stripe = useStripe();
    const elements = useElements();
    const [error, setError] = useState<string | null>(null);
    const [processing, setProcessing] = useState(false);

    const handleSubmit = async (e: React.MouseEvent) => {
        e.preventDefault();
            if (!stripe || !elements)  {
                return;
            } else {
                setProcessing(true);
                const { error } = await stripe.confirmPayment({
                    elements,
                    confirmParams: {
                        return_url: window.location.origin + "/payment-success",
                    },
                });

                if (error) {
                    setError(error.message ?? "Payment failed");
                    setProcessing(false);
                }
        }
    };

    return (
        <div>
            <PaymentElement
                options={{
                    fields: {
                    billingDetails: {
                        name: "always",
                    },
                    },
                }}
                />

            <button onClick={handleSubmit} disabled={!stripe || processing}>
                {processing ? "Processing…" : "Pay"}
            </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );

}

export default StripePaymentPage;