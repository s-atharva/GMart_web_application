<template>
    <div class="header-container">
        <div>
            <h1 class="page-header">Hello {{ user.username }}</h1>
        </div>
        <div>
            <h1 class="page-header">Order Details</h1>
        </div>
        <div class="navigation">
            <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
            <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>
    <div id="pdf-content" class="invoice-box">
        <h1 style="padding: 15px; text-align: center">Order Details</h1>
        <p style="text-align: center; font-weight: bold" >Order ID: {{ orderId }}</p>
        <p style="text-align: center">Ordered at {{ formateOrderData(createdAt) }}</p>


        <div style="text-align: center">
            <p>Address: {{ addressInfo.address }}, {{ addressInfo.city }} {{ addressInfo.pincode }},
                {{ addressInfo.state }}</p>
        </div>

        <p class="product-header-detail">Products List:</p>

        <ul class="product-list">
            <li v-for="product in productsInfo" :key="product.name" style="text-align: center; list-style-type: none;">
                {{ product.name }} - Count: {{ product.count }} - Price: Rs. {{ product.price }}
            </li>
        </ul>

        <p class="total-amount" style="text-align: center" >Total Order Amount: Rs.{{ totalOrderAmount }}</p>
        <button @click="generatePdf" class="btn btn-success pdf-button">Download PDF</button>
    </div>
</template>

<script>
import axios from "axios";
import moment from "moment/moment";
import html2pdf from "html2pdf.js/src";

export default {
    name: 'orderDetails',
    data() {
        return {
            orderId: '',
            createdAt: '',
            addressInfo: '',
            totalOrderAmount: '',
            productsInfo: []
        }
    },
    created() {
        this.orderId = this.$route.params.orderId
    },
    mounted() {
        this.getDetails()
    },
    methods: {
        generatePdf() {
            // Wait for the next tick to ensure that the DOM has been updated
            const element = document.getElementById("pdf-content");
            console.log("element: ", element)

            // Customize the options for html2pdf
            const options = {
                margin: 20,
                marginTop: -10,
                filename: "orders.pdf",
                image: {type: "jpeg", quality: 0.98},
                html2canvas: {scale: 3},
                jsPDF: {unit: "mm", format: "a4", orientation: "landscape"},
            };

            // Use html2pdf to generate the PDF
            html2pdf(element, options);

        },
        formateOrderData(date) {
            return moment(date).format('DD MMM, YYYY hh:mm:ss A')
        },
        getDetails() {
            axios.get(`http://127.0.0.1:8005/user/${this.user.user_id}/orders/${this.orderId}`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log(response.data)
                    this.orderId = response.data.order_id
                    this.createdAt = response.data.created_at
                    this.addressInfo = response.data.address_info
                    this.totalOrderAmount = response.data.total_order_amount
                    this.productsInfo = response.data.products_info
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
.invoice-box{
    display: compact;
    align-items: center;
}
.container-order {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 10%;
    border: 2px solid #d41b1b;
    box-sizing: border-box;
    margin-left: 33%;
    width: 30%;
}

.section-divider,
.item-divider {
    border: 5px solid #ee6565;
    margin: 10px 0;
}

.pdf-button {
    position: fixed;
    bottom: 80px;
    margin-left: 6%;
}

.product-header-detail {
    text-align: center;
    color: #e92525;
}
.product-list {
    text-align: center;
}
</style>