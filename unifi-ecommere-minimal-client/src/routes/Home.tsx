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
                    <li>
                        Create webmaster
                    </li>
                </ul>
                <hr inert/>

                <ul aria-label="Login">
                    <li>
                        <Link to="/login">
                            Login
                        </Link>
                    </li>
                    <li>
                        Refresh JWT token
                    </li>
                </ul>

                <hr inert/>

                <ul aria-label='User endpoints'>
                    <li>
                        <Link to="/list-users">
                            List all users by role
                        </Link>
                    </li>
                    <li>
                        Update user info
                    </li>
                    <li>
                        List all roles
                    </li>
                </ul>

                <hr inert/>
                <ul aria-label="Category endpoints">
                    <li>
                        <Link to="/create-category">
                            Create a new category
                        </Link>
                    </li>
                    <li>
                        List all categories
                    </li>
                </ul>
                <hr inert/>

                <ul aria-label="Product endpoints">
                    <li>
                        <Link to="/create-product">
                            Create a new product
                        </Link>
                    </li>
                    <li>
                        Restock an existing product
                    </li>
                    <li>
                        List all products
                    </li>
                    <li>
                        List all products for a category
                    </li>
                    <li>
                        Update product info
                    </li>
                    <li>
                        Soft delete a product
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
                            CRUD cart
                        </Link>
                    </li>
                    <li>
                        Place a new order
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