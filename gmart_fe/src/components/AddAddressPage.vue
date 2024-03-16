<template>
    <div class="header-container">
        <div>
            <h1 class="page-header">Hello {{ user.username }}</h1>
        </div>
        <div class="navigation">
            <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
            <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>

    <div class="addAddress">
        <h1>Add Address</h1>
        <br>
        <form v-on:submit.prevent="addAddress">
            <div class="form-group">
                <label for="categoryName">Address</label>
                <input type="text" class="form-control" id="categoryName" v-model="address" required>
            </div>
            <div class="form-group">
                <label for="ImageAddress">City</label>
                <input type="text" class="form-control" id="ImageAddress" v-model="city" required>
            </div>
            <div class="form-group">
                <label for="ImageAddress">Pincode</label>
                <input type="text" class="form-control" id="ImageAddress" v-model="pincode" required>
            </div>
            <div class="form-group">
                <label for="ImageAddress">State</label>
                <input type="text" class="form-control" id="ImageAddress" v-model="state" required>
            </div>

            <button type="submit" class="btn btn-success">Add</button>
        </form>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'AddAddressPage',
    data() {
        return {
            address: '',
            city: '',
            state: '',
            pincode: ''
        }
    },
    methods: {
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/customer/login')
        },
        addAddress() {
            const result = axios.post(`http://127.0.0.1:8005/address/${this.user.user_id}`, {
                address: this.address,
                city: this.city,
                state: this.state,
                pincode: this.pincode
            }, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
            console.log(result)
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
    background-color: #fff; /* Optional: Set a background color if needed */
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
    max-width: 500px; /* Set a maximum width for larger screens */
    margin-bottom: 16px;
}

.card-img {
    width: 100%;
    height: 160px;
    object-fit: contain; /* Use 'contain' to fit the entire image within the container */
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

body {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 75vh;
    margin: 0;
}

.addAddress {
    background-color: #4955fa;
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    margin-top: -20px;
}

form {
    max-width: 400px;
    margin: 0 auto;
}
</style>