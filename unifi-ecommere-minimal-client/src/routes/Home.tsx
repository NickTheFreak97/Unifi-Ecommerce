import React from 'react'
import { Link } from 'react-router'



const Home: React.FC = () => {
    return (
        <main>
            <h1>
                Ecommerce REST API minimal client
            </h1>
            <nav>
                <ul aria-label="sign up">
                    <li>
                        <Link to="/customer-signup">
                            Create Customer
                        </Link>
                    </li>
                    <li>
                        <Link to="/shop-staff-signup">
                            Create store manager
                        </Link>
                    </li>
                </ul>
                <hr inert/>

                <ul aria-label="Login">
                    <li>
                        <Link to="/login">
                            Login
                        </Link>
                    </li>
                </ul>

                <hr inert/>

                <ul aria-label='User endpoints'>
                    <li>
                        <Link to="/list-users">
                            List all users by role
                        </Link>
                    </li>
                </ul>

                <hr inert/>
                <ul aria-label="Category endpoints">
                    <li>
                        <Link to="/create-category">
                            Create a new category
                        </Link>
                    </li>
                </ul>
                <hr inert/>

                <ul aria-label="Product endpoints">
                    <li>
                        <Link to="/create-product">
                            Create a new product
                        </Link>
                    </li>
                </ul>

                <hr inert/>
                <ul aria-label="Ordering">
                    <li>
                        <Link to="/catalog">
                            View Catalog
                        </Link>
                    </li>
                    <li>
                        <Link to="/cart">
                            Manage cart | Create & Update order | Pay
                        </Link>
                    </li>
                </ul>

                <hr inert/>
                <ul aria-label='payment methods'>
                    <li>
                        <Link to="/create-payment-method">
                            Create a payment method
                        </Link>
                    </li>
                </ul>
            </nav>
        </main>
    )
}

export default Home