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
                        Login
                    </li>
                    <li>
                        Refresh JWT token
                    </li>
                </ul>

                <hr inert/>

                <ul aria-label='User endpoints'>
                    <li>
                        List all users by role
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
                        Create a new category
                    </li>
                    <li>
                        List all categories
                    </li>
                </ul>

                <ul aria-label="Product endpoints">
                    <li>
                        Create a new product
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
                        Place a new order
                    </li>
                </ul>
            </nav>
        </main>
    )
}

export default Home