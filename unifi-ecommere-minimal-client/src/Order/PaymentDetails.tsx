import { loadStripe } from "@stripe/stripe-js";
import { Elements, PaymentElement, useStripe, useElements } from "@stripe/react-stripe-js";
import { useState, useEffect, useRef } from "react";
import { v4 as uuidv4 } from "uuid";


const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY);


const PaymentDetails: React.FC = () => {
    return (
        <main>
        
        </main>
    )
}

export default PaymentDetails;