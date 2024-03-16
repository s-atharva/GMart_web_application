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

    <div v-if="showAddressAlert" class="alert alert-danger" role="alert">
        Please select an Address
    </div>
    <h3>Select a Address</h3>
    <div v-for="address in addresses" :key="address.address" class="address-radio">
        <label>
            <input type="radio" v-model="selectedAddress" :value="address" name="selectedAddress">
            {{ address.address }}, {{ address.city }}, {{ address.pincode }}, {{ address.state }}
        </label>
    </div>


    <button @click="finalizeOrder" class="btn btn-primary mr-2">Finalize Order</button>
    <button @click="goToAddressPage" class="btn btn-primary">Add new Address</button>

</template>

<script>

import axios from "axios";

export default {
    name: 'AddressPage',
    data() {
        return {
            addresses: [],
            selectedAddressId: '',
            selectedAddress: null,
            showAddressAlert: false,
        }
    },
    mounted() {
        this.getAddresses()
    },
    methods: {
        getAddresses() {
            axios.get(`http://127.0.0.1:8005/users/${this.user.user_id}/addresses`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    this.addresses = response.data.map(addressItem => {
                        return {
                            addressId: addressItem.address_id,
                            address: addressItem.address,
                            city: addressItem.city,
                            pincode: addressItem.pincode,
                            state: addressItem.state
                        }
                    })
                    console.log(this.addresses)
                })
                .catch(error => {
                    console.error('Error fetching addresses:', error)
                })
        },
        finalizeOrder() {
            if (this.selectedAddress === null) {
                this.showAddressAlert = true
                setTimeout(() => {
                    this.showAddressAlert = false
                }, 3000)
            } else {
                // this.$router.push('/summaryPage')
                const addressId = this.selectedAddress.addressId
                axios.put(`http://127.0.0.1:8005/users/${this.user.user_id}/address`, {
                    current_address_id: addressId
                }, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                    .then(response => {
                        console.log('Address updated successfully', response);
                        this.$router.push('/summaryPage')
                    })
                    .catch(error => {
                        console.error('Error updating address:', error)
                    })
            }
        },
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/customer/login')
        },
        goToAddressPage() {
            this.$router.push('/address/add')
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

.address-radio {
    margin-bottom: 10px;
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


.address-radio {
    margin-bottom: 10px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #f9f9f9;
}

.address-radio label {
    display: block;
    padding: 5px;
}

/* Style the selected radio button label */
.address-radio label input:checked {
    background-color: #3490dc;
    color: white;
}

/* Style the hover effect for radio buttons */
.address-radio label:hover {
    background-color: #e2e8f0;
    cursor: pointer;
}

.btn {
    cursor: pointer;
}
</style>