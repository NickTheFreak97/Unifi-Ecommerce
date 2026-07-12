import React, { useState, useRef, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";
import { loadStripe } from "@stripe/stripe-js";
import { Elements, PaymentElement, useStripe, useElements } from "@stripe/react-stripe-js";

const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLIC_KEY);

const StripePaymentPage: React.FC = ( ) => {
        const [clientSecret, setClientSecret] = useState("");
        const idempotencyKey = useRef(uuidv4()).current;

        useEffect(() => {
            fetch("/api/create-payment-intent/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                amount: 2000,
                idempotency_key: idempotencyKey,
            }),
            })
            .then((r) => r.json())
            .then((data) => setClientSecret(data.client_secret));
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
            <PaymentElement />
            <button onClick={handleSubmit} disabled={!stripe || processing}>
                {processing ? "Processing…" : "Pay"}
            </button>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );

}

