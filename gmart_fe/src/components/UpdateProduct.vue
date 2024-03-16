<template>
    <div class="header-container-manager">
        <div>
            <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
        </div>
        <div class="navigation">
            <router-link to="/manager/dashboard" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/manager/requestCategory" class="btn btn-secondary mr-2">Request new Category</router-link>
            <router-link to="/manager/addProduct" class="btn btn-primary mr-2">Add new Product</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>
    <div class="updateProduct-manager">
        <h1>Update Product</h1>
        <br>
        <form @submit.prevent="updateProduct">
            <div class="form-group">
                <label for="productName">Product Name</label>
                <input v-model="productName" type="text" class="form-control" id="productName" required>
            </div>

            <div class="form-group">
                <label for="productDescription">Description</label>
                <input v-model="productDescription" type="text" class="form-control" id="productDescription" required>
            </div>

            <div class="form-group">
                <label for="productPrice">Price</label>
                <input v-model="productPrice" type="text" class="form-control" id="productPrice" required>
            </div>

            <div class="form-group">
                <label for="productStock">Stock</label>
                <input v-model="productStock" type="text" class="form-control" id="productStock" required>
            </div>

            <div class="form-group">
                <label for="productWeight">Weight</label>
                <input v-model="productWeight" type="text" class="form-control" id="productWeight" required>
            </div>

            <div class="form-group">
                <label for="productImage">Image Path</label>
                <input v-model="productImage" type="text" class="form-control" id="productImage" required>
            </div>

            <button type="submit" class="btn btn-success">Update</button>
        </form>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'UpdateProduct',
    data() {
        return {
            productId: '',
            categoryId: '',
            productName: '',
            productDescription: '',
            productPrice: '',
            productStock: '',
            productWeight: '',
            productImage: '',
            status: 'ACTIVE'

        }
    },
    created() {
        this.productId = this.$route.params.productId
        this.categoryId = this.$route.params.categoryId
    },
    methods: {
        updateProduct() {
            const data = {
                name: this.productName,
                description: this.productDescription,
                price: this.productPrice,
                stock: this.productStock,
                weight: this.productWeight,
                image_path: this.productImage,
                status: this.status
            }
            axios.put(`http://127.0.0.1:8005/categories/${this.categoryId}/product/${this.productId}`, data, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log('Product updated successfully', response.data)
                    this.$router.push(`/manager/category/${this.categoryId}/products`)
                })
                .catch(error => {
                    console.error("error updating product", error)
                })
        },
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/manager/login')
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
.updateProduct-manager {
    background-color: #158bd6;
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 50px rgb(47, 145, 235);
    margin-top: 80%;
}
</style>