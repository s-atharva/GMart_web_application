<template>
    <div class="header-container-admin">
        <div>
            <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
        </div>
        <div class="navigation">
            <router-link to="/categories" class="btn btn-primary mr-2">Home</router-link>

            <router-link to="/categories/requested" class="btn btn-secondary mr-2">Requested Categories</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>

    <div class="addCategory">
        <h1>Add Category</h1>
        <br>
        <form v-on:submit.prevent="addCategory">
            <div class="form-group">
                <label for="categoryName">Category Name</label>
                <input type="text" class="form-control" id="categoryName" v-model="categoryName" required>
            </div>
            <div class="form-group">
                <label for="ImageAddress">Description</label>
                <input type="text" class="form-control" id="ImageAddress" v-model="categoryDescription" required>
            </div>
            <div class="form-group">
                <label for="ImageAddress">Image</label>
                <input type="text" class="form-control" id="ImageAddress" v-model="imagePath" required>
            </div>
            <button type="submit" class="btn btn-success mr-2">Add</button>
            <button @click="backToHome" class="btn btn-secondary">Back</button>
        </form>
    </div>
</template>

<script>
import axios from "axios"

export default {
    name: 'AddCategories',
    data() {
        return {
            categoryName: '',
            categoryDescription: '',
            imagePath: ''
        }
    },
    methods: {
        async addCategory() {
            const result = await axios.post('http://127.0.0.1:8005/categories/add', {
                name: this.categoryName,
                description: this.categoryDescription,
                image_path: this.imagePath,
                status: 'ACTIVE'
            }, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
            console.log(result)
            this.$router.push('/categories')
        },
        backToHome() {
            this.$router.push('/categories')
        },
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/admin/login')
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
body {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 75vh;
    margin: 0;
}

.addCategory {
    background-color: #4955fa;
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    margin-top: 30%;
}

form {
    max-width: 400px;
    margin: 0 auto;
}
</style>