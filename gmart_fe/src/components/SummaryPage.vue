<template>
    <div class="page-container">
        <div class="header-container">
            <div>
                <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
            </div>
            <div class="navigation">
                <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
                <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
                <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
                <button @click="logout" class="btn btn-success">Logout</button>
            </div>
        </div>
        <div id="pdf-content" class="scrollable-box">
            <div v-if="userInfo && cartInfo" class="content-container">
                <div class="user-details">
                    <h2>User Information</h2>
                    <p>Name: {{ userInfo.firstName }} {{ userInfo.lastName }}</p>
                </div>
                <hr class="section-divider">

                <div class="shipping-address">
                    <h2>Shipping Address</h2>
                    <p>Address: <span>{{ addressInfo.address }}, {{ addressInfo.city }}, {{
                            addressInfo.pincode
                        }}</span>
                    </p>
                    <p>State: {{ addressInfo.state }}</p>
                </div>
                <hr class="section-divider">

                <div class="order-details">
                    <h2>Order Details</h2>
                    <div v-for="(item, index) in productDetails" :key="index" class="order-item">
                        <p>Product Name: {{ item.name }}</p>
                        <p>Total: {{ item.price }} * {{ item.count }}</p>
                        <span>Rs.{{ calculateTotal(item) }}</span>
                        <hr class="item-divider">
                    </div>

                    <div class="total-price">
                        Overall Cart Amount: Rs.{{ calculateOverallTotal() }}
                    </div>
                </div>
            </div>

            <div v-else class="no-info-container">
                <p>No information available.</p>
            </div>
        </div>
        <button @click="proceedToPayment" class="btn btn btn-info fixed-bottom">Proceed to Payment</button>
    </div>

</template>

<script>
import axios from "axios";
import html2pdf from "html2pdf.js/src";

export default {
    name: 'SummaryPage',
    data() {
        return {
            info: [],
            userInfo: {},
            addressInfo: {},
            cartInfo: [],
            productDetails: [],

        }
    },
    mounted() {
        this.getCartSummary()
    },
    methods: {
        generatePdf() {
            const element = document.getElementById('pdf-content')
            html2pdf(element)
        },
        proceedToPayment() {
            const user_id = this.user.user_id
            axios.post(`http://127.0.0.1:8005/user/${user_id}/place_order`, {}, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log(response.data)
                    console.log(user_id)
                    this.$router.push('/orders')
                })
                .catch(error => {
                    console.error('Error placing order:', error);
                    // Handle the error if needed
                })

        },
        calculateTotal(item) {
            return item.price * item.count;
        },
        calculateOverallTotal() {
            let total = 0;
            for (const item of this.productDetails) {
                total += this.calculateTotal(item)
            }
            return total;
        },
        getCartSummary() {
            axios.get(`http://127.0.0.1:8005/user/${this.user.user_id}/cart_summary`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    this.info = response.data
                    const userInformation = response.data.user_info
                    this.userInfo = {
                        firstName: userInformation.first_name,
                        lastName: userInformation.last_name,
                    }
                    const userAddressInformation = response.data.address_info
                    this.addressInfo = {
                        address: userAddressInformation.address,
                        city: userAddressInformation.city,
                        pincode: userAddressInformation.pincode,
                        state: userAddressInformation.state
                    }
                    this.cartInfo = response.data.user_info.user_metadata.cart_info.map(item => {
                        return {
                            productId: item.product_id,
                            count: item.count,
                        }
                    })
                    this.getProductDetails()
                    console.log(this.cartInfo)

                })
                .catch(error => {
                    console.error('Error fetching info:', error)
                })
        },
        getProductDetails() {
            this.productDetails = []; // Reset productDetails array
            this.productCountList = {}; // Initialize an object to store counts for each productId

            // Create an array of promises for fetching product details
            const promises = this.cartInfo.map(product => {
                return axios.get(`http://127.0.0.1:8005/product/${product.productId}`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                    .then(response => {
                        const productId = response.data.product_id;
                        const count = product.count;

                        // Store count for the productId in the list
                        if (!this.productCountList[productId]) {
                            this.productCountList[productId] = [];
                        }
                        this.productCountList[productId].push(count);

                        return {
                            productId,
                            name: response.data.name,
                            price: response.data.price,
                            stock: response.data.stock,
                            image: response.data.image_path,
                            description: response.data.description,
                            count: product.count
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching product details:', error)
                        return null; // Handle errors gracefully
                    })
            })

            // Resolve all promises and update productDetails array
            Promise.all(promises)
                .then(details => {
                    this.productDetails = details.filter(detail => detail !== null);
                    console.log(this.productCountList); // Log the product count list
                })
                .catch(error => {
                    console.error('Error resolving product details promises:', error)
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
.page-container {
    max-width: 800px;
    margin: auto;
    padding: 200px;
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
    margin-left: 10px;
    margin-top: 10%;
}

.navigation {
    margin: 0; /* Remove default margin for h1 element */
    width: 20%
}

.content-container {
    margin-top: 20px;
}


.user-details {
    margin-bottom: 10%;
}

.shipping-address {
    margin-bottom: 10%;
}

.order-details {
    margin-bottom: 10%;
}

.pdf-button {
    position: fixed;
    bottom: 20px;
    left: 41%;
}

.scrollable-box {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(90vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 0.5rem 16px 16px;
    margin-top: 10%;
    width: 100%;
    border: 2px solid #e9e0e0;
}

.section-divider,
.item-divider {
    border: 5px solid #ee6565;
    margin: 10px 0;
}

.total-price {
    margin-top: 20px;
    text-align: center;
}

.no-info-container {
    margin-top: 20px;
    text-align: center;
}

.btn {
    padding: 10px 10px;
}

.btn-primary {
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.btn-secondary {
    background-color: #ff6a00;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.btn-success {
    background-color: #28a745;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.fixed-bottom {
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 15%;
}
</style>