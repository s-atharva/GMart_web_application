<template>
    <div class="header-container">
        <div>
            <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
        </div>
        <div>
            <h1 class="page-header">Cart</h1>
        </div>
        <div class="navigation">
            <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
            <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>
    <div class="card-container">
        <!--        <h2 class="section-title">Cart</h2>-->
        <div v-for="product in cart" :key="product.productId" class="card">
            <img class="card-img" :src="product.image"
                 style="width: 103%; height: 200px; object-fit: contain">
            <div class="card-body">
                <h5 class="card-title">Name: {{ product.name }}</h5>
                <p class="card-description">Price: Rs.{{ product.price }}</p>
                <p class="card-description">Stock: {{ product.quantity }}</p>
                <p class="card-price">Total: {{ product.price }} * {{ product.quantity }} : Rs.
                    {{ calculateTotal(product) }}</p>
                <button @click="removeFromCart(product.productId)" class="btn btn-danger">Remove</button>
            </div>
        </div>
    </div>
    <div class="total-price">
        Overall Cart Amount: Rs.{{ calculateOverallTotal() }}
    </div>

    <button @click="goToAddressPage" class="btn btn-success" :disabled="calculateOverallTotal() === 0">Proceed to
        Checkout
    </button>

</template>

<script>
import axios from "axios";

export default {
    name: 'CustomerCartPage',
    data() {
        return {
            cart: []
        }
    },
    mounted() {
        this.getCart()
    },
    methods: {
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/customer/login')
        },
        calculateTotal(product) {
            return product.price * product.quantity
        },
        calculateOverallTotal() {
            return this.cart.reduce((total, product) => total + this.calculateTotal(product), 0)
        },
        getCart() {
            axios.get(`http://127.0.0.1:8005/cart/${this.user.user_id}`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    const cartWithDetails = response.data.map(async product => {
                        // Fetch detailed product information based on productId
                        const productDetails = await axios.get(`http://127.0.0.1:8005/product/${product.product_id}`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}});

                        return {
                            productId: product.product_id,
                            quantity: product.count,
                            name: productDetails.data.name,
                            price: productDetails.data.price,
                            stock: productDetails.data.stock,
                            image: productDetails.data.image_path,
                            description: productDetails.data.description
                        };
                    });

                    // Wait for all product details to be fetched before updating cart
                    Promise.all(cartWithDetails).then(cartDetails => {
                        this.cart = cartDetails;
                    });

                    console.log(response.data);
                })
                .catch(error => {
                    console.error("Error fetching cart:", error);
                });
        },
        removeFromCart(productId) {
            axios.delete(`http://127.0.0.1:8005/user/${this.user.user_id}/cart`, {
                    data: {product_id: productId}, headers: {"Authorization": `Bearer ${this.user.access_token}`}
                }
            )
                .then(response => {
                    console.log(response.data)
                    this.getCart()
                })
                .catch(error => {
                    console.error(error)
                })
        },
        goToAddressPage() {
            this.$router.push('/address')
        }
    },
    computed: {
        user() {
            // Retrieve user information from session storage
            const userData = sessionStorage.getItem('user')
            return userData ? JSON.parse(userData) : null
        }
    }
}
</script>


<style>
.page-container {
    flex-direction: column;
    margin-top: 30px;
    height: 100vh;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #e92525; /* Optional: Set a background color if needed */
    z-index: 1000; /* Ensure the header is above other elements */
}

.page-header {
    width: 100%;
    text-align: center;
    margin-left: 100px;
    margin-top: 5%;
}

.navigation {
    margin: 0; /* Remove default margin for h1 element */
    width: 20%
}


.card-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 30%;
}

.section-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 16px;
    width: 100%;
}

.card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 300px;
    max-width: 500px;
    margin-bottom: 16px;
}

.card-img {
    width: 100%;
    height: 160px;
    object-fit: scale-down;
}

.card-body {
    padding: 16px;
}

.card-title {
    text-align: left;
    font-size: 18px;
    margin-bottom: 18px;
    margin-left: 20px;
}

.card-price {
    font-weight: bold;
    color: green;
    margin-left: 20px;
    text-align: left;
}

.total-price {
    font-weight: bold;
    color: green;
}

.card-description {
    text-align: left;
    margin-left: 20px;
    margin-bottom: 12px;
    align-content: start;
}

.buy-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.btn {
    cursor: pointer;
}
</style>