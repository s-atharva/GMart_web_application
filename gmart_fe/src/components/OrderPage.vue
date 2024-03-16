<template>
    <div class="header-container">
        <div>
            <h1 class="page-header">Hello {{ user.username }}</h1>
        </div>
        <div>
            <h1 class="page-header">Your Orders</h1>
        </div>
        <div class="navigation">
            <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
            <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>
    <div id="pdf-content" class="container-orders">
        <h1 class="section-title">Order History</h1>
        <div v-for="order in orders" :key="order.order_id">
            <hr class="section-divider">
            <router-link :to="{name:'orderDetails', params: { orderId: order.orderId }}">
                <p class="orderId">Order ID: {{ order.orderId }}</p>
            </router-link>
            <hr class="section-divider">
            <p>Ordered at {{ formateOrderData(order.createdAt) }}</p>
            <div v-if="order.addressInfo">
                <p>Address: {{ order.addressInfo.address }}, {{ order.addressInfo.city }} {{
                        order.addressInfo.pincode
                    }}, {{ order.addressInfo.state }}</p>
            </div>


            <p class="product-header">Products List:</p>
            <ul class="product-list">
                <li v-for="product in order.productsInfo" :key="product.name">
                    {{ product.name }} - Count: {{ product.count }} - Price: {{ product.price }}
                </li>

            </ul>

            <p class="total-amount">Total Order Amount: Rs.{{ order.totalOrderAmount }}</p>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import moment from "moment"

export default {
    name: 'OrderPage',
    data() {
        return {
            orders: []
        }
    },
    mounted() {
        this.getDetails()
    },
    methods: {
        formateOrderData(date) {
            return moment(date).format('DD MMM, YYYY hh:mm:ss A')
        },
        getDetails() {
            axios.get(`http://127.0.0.1:8005/user/${this.user.user_id}/orders`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log(response.data)
                    this.orders = response.data.map(order => ({
                        orderId: order.order_id,
                        createdAt: order.created_at,
                        addressInfo: order.address_info,
                        totalOrderAmount: order.total_order_amount,
                        productsInfo: order.products_info
                    }))
                })

        },
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/customer/login')
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
.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #1a93f6;
    z-index: 110000;
}

.container-orders {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 15%;
    border: 2px solid #d41b1b;
    box-sizing: border-box;
    margin-left: 33%;
    width: 30%;
}

.section-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 16px;
    width: 100%;
    font-family: "Lucida Console", "Courier New", monospace;
}

.pdf-button {
    position: fixed;
    bottom: 80px;
    margin-left: 2%;
}

.orderId {
    font-weight: bold;
}

.product-list {
    text-align: left;
}

.total-amount {
    color: #6634e8;
}

.product-header {
    color: #e92525;
}
</style>