<template>

    <div class="header-container-manager">
        <div>
            <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
        </div>
        <div class="navigation">
            <router-link to="/manager/dashboard" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/manager/requestCategory" class="btn btn-secondary mr-2">Request new Category</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>

    <div class="addProduct-manager">
        <h1>Add Products</h1>
        <br>
        <form @submit.prevent="addCategory">
            <div class="form-group">
                <label for="productName">Product Name</label>
                <input type="text" class="form-control" id="productName" v-model="categoryName" required>
            </div>
            <div class="form-group">
                <label for="category">Category</label>
                <select class="form-control" id="category" v-model="selectedCategory" required>
                    <option v-for="category in categories" :key="category.categoryId" :value="category.categoryId">
                        {{ category.name }}
                    </option>
                </select>
            </div>
            <div class="form-group">
                <label for="productDescription">Description</label>
                <input type="text" class="form-control" id="productDescription" v-model="categoryDescription" required>
            </div>
            <div class="form-group">
                <label for="price">Price</label>
                <input type="text" class="form-control" id="price" v-model="price" required>
            </div>
            <div class="form-group">
                <label for="stock">Stock</label>
                <input type="text" class="form-control" id="stock" v-model="stock" required>
            </div>
            <div class="form-group">
                <label for="weight">Weight</label>
                <input type="text" class="form-control" id="weight" v-model="weight" required>
            </div>
            <div class="form-group">
                <label for="imagePath">Image</label>
                <input type="text" class="form-control" id="imagePath" v-model="imagePath" required>
            </div>
            <button type="submit" class="btn btn-success mr-2">Add</button>
            <router-link to="/manager/dashboard" class="btn btn-secondary">Back</router-link>
        </form>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'ManagerAddProducts',
    data() {
        return {
            categories: [],
            categoryId: '',
            categoryName: '',
            selectedCategory: '',
            categoryDescription: '',
            price: '',
            stock: '',
            weight: '',
            imagePath: ''
        }
    },
    mounted() {
        this.getCategories();
    },
    methods: {
        getCategories() {
            axios.get('http://127.0.0.1:8005/categories', {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    this.categories = response.data.map(category => {
                        return {
                            categoryId: category.category_id,
                            name: category.name,
                            description: category.description,
                            image_path: category.image_path
                        }
                    })
                    console.log(this.categories)
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                })
        },
        addCategory() {
            const data = {
                category_id: this.selectedCategory,
                name: this.categoryName,
                description: this.categoryDescription,
                price: this.price,
                stock: this.stock,
                weight: this.weight,
                image_path: this.imagePath,
                status: 'ACTIVE'
            }
            axios.post(`http://127.0.0.1:8005/categories/${this.selectedCategory}/product`, data, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    // Handle the response, if needed
                    console.log(response);
                    this.$router.push('/manager/dashboard')
                })
                .catch(error => {
                    // Handle errors
                    console.error('Error adding product:', error);
                });
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
.addProduct-manager {
    background-color: rgb(47, 145, 235);
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 100px rgb(47, 145, 235);
    margin-top: 120%;
    margin-bottom: 10%;
}
</style>