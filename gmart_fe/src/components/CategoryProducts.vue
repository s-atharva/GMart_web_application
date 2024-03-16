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
    <div class="products-container-manager">
        <div v-if="products.length === 0">
            <H2>No Products</H2>
        </div>
        <div v-for="product in products" :key="product.productId" class="card" style="width: 18rem">
            <img class="card-img" :src="product.imagePath"
                 style="width: 100%; height: 250px; object-fit: fill">
            <div class="card-body">
                <h5 class="card-title">{{ product.name }}</h5>
                <p class="card-description">{{ product.description }}</p>
                <router-link
                    :to="{ name: 'UpdateProduct' , params: { categoryId: product.categoryId,productId: product.productId}}"
                    class="btn btn-primary mr-2">Update
                </router-link>
                <button @click="deleteProduct(categoryId, product.productId)" class="btn btn-danger">Delete</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'CategoryProducts',
    data() {
        return {
            categoryId: '',
            categoryName: '',
            products: []
        }
    },
    created() {
        this.categoryId = this.$route.params.categoryId
        this.categoryName = this.$route.params.categoryName
    },
    mounted() {
        this.getProductsByCategory()
    },
    methods: {
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
                            imagePath: product.image_path
                        }
                    })
                    console.log(response)
                })
        },
        deleteProduct(categoryId, productId) {
            axios.delete(`http://127.0.0.1:8005/category/${categoryId}/product/${productId}`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log("Product deleted successfully", response.data)
                    this.getProductsByCategory()
                })
                .catch(error => {
                    console.error('Error deleting category:', error);
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
.products-container-manager {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 12%;
    border: 2px solid #ffffff;
    box-sizing: border-box;
    width: 100%;
}

.card {
    width: 18rem;
    border: 1px solid #ccc;
    border-radius: 8px;
    overflow: hidden;
}

.card-img {
    width: 100%;
    height: 150px;
    object-fit: cover;
}

.card-body {
    padding: 1rem;
}

.btn {
    margin-top: 0.5rem;
}
</style>