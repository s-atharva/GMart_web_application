<template>
    <div class="header-container">
        <div>
            <h1 class="page-header">Hello {{ user.username }}</h1>
        </div>
        <div class="search-input">
            <input v-model="searchQuery" class="form-control mr-sm-2" type="search" placeholder="Search Products">
        </div>
        <div class="navigation">
            <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
            <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>

    <div v-if="products.length > 0" class="products-container">
        <div v-for="product in products" :key="product.productId" class="card">
            <img class="card-img" :src="product.imagePath">
            <div class="card-body">
                <h5 class="card-title">Name: {{ product.name }}</h5>
                <p class="card-description-customer-products">Price: Rs.{{ product.price }}</p>
                <p class="card-description-customer-products">Description: {{ product.description }}</p>
                <p v-if="product.stock < 20 & product.stock>1" class="card-few-stock">Only {{ product.stock }}
                    remaining!!</p>
                <p v-else-if="product.stock === 0" class="card-few-stock">Out of stock!!</p>
                <p v-else class="card-few-stock"><br></p>

                <div class="quantity-controls">
                    <button @click="decrementQuantity(product)" class="btn btn btn-secondary mr-2">-</button>
                    <button @click="incrementQuantity(product)" class="btn btn btn-secondary mr-2">+</button>
                    <button class="btn btn-primary mr-2">{{ product.quantity }}</button>
                    <button @click="addToCart(product)" class="btn btn-warning" :disabled="product.quantity === 0">Add
                        to Cart
                    </button>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <h2>No Products</h2>
    </div>
    <div v-if="showCartAlert" class="alert alert-success" role="alert">Added to Cart</div>
</template>

<script>
import axios from "axios";

export default {
    name: 'CustomerProductsPage',
    props: ['categoryId', 'categoryName'],
    data() {
        return {
            products: [],
            showCartAlert: false,
            searchQuery: ''
        }
    },
    mounted() {
        this.getProductsByCategory()
    },
    watch: {
        searchQuery: 'getProductsByCategory'
    },
    methods: {
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/customer/login')
        },
        incrementQuantity(product) {
            if (product.quantity < product.stock) {
                product.quantity += 1;
            } else {
                console.log(`Cannot increment quantity beyond stock limit of ${product.stock}`);
            }
        },
        decrementQuantity(product) {
            if (product.quantity && product.quantity > 0) {
                product.quantity -= 1;
            }
        },
        addToCart(product) {
            const data = {
                product_id: product.productId,
                count: product.quantity
            }
            console.log('Adding to cart:', data)
            if (this.user) {
                console.log(this.user)
            }
            axios.post(`http://127.0.0.1:8005/user/${this.user.user_id}/cart`, data, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log("Cart updated successfully", response.data)
                    this.showCartAlert = true
                    setTimeout(() => {
                        this.showCartAlert = false
                    }, 3000)
                })
                .catch(error => {
                    console.error("Error updating Cart", error)
                })
        },
        getProductsByCategory() {
            axios.get(`http://127.0.0.1:8005/category/${this.categoryId}/products`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    this.products = response.data.map(product => {
                        return {
                            productId: product.product_id,
                            name: product.name,
                            description: product.description,
                            price: product.price,
                            stock: product.stock,
                            weight: product.weight,
                            imagePath: product.image_path,
                            quantity: 0
                        }
                    })
                    if (this.searchQuery) {
                        const searchRegex = new RegExp(this.searchQuery, 'i');
                        this.products = this.products.filter(product => searchRegex.test(product.name));
                    }
                    console.log(response)
                })
        },

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
.products-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 15%;
    border: 2px solid #f3e7e7;
    box-sizing: border-box;
    width: 80%;
    margin-left: 10%;
}

.card-few-stock {
    text-align: left;
    margin-left: 20px;
    margin-bottom: 12px;
    align-content: start;
    color: #e92525;
}

.card-description-customer-products {
    text-align: left;
    margin-left: 20px;
    margin-bottom: 12px;
    align-content: start;
}
</style>