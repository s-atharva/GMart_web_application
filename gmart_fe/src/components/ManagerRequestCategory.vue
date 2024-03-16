<template>
    <div class="header-container-manager">
        <div>
            <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
        </div>
        <div class="navigation">
            <router-link to="/manager/dashboard" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/manager/addProduct" class="btn btn-primary mr-2">Add new Product</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>
    <div class="addCategory-manager">
        <h1>Add Category Request</h1>
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
            <button type="submit" class="btn btn-success">Add</button>
        </form>
    </div>
</template>

<script>
import axios from "axios"

export default {
    name: 'ManagerRequestCategory',
    data() {
        return {
            categoryName: '',
            categoryDescription: '',
            imagePath: '',
        }
    },
    methods: {
        async addCategory() {
            const result = await axios.post('http://127.0.0.1:8005/categories/add', {
                name: this.categoryName,
                description: this.categoryDescription,
                image_path: this.imagePath,
                status: 'REQUESTED'
            }, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
            console.log(result)
            this.$router.push('/manager/dashboard')
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
body {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 75vh;
    margin: 0;
}

.addCategory-manager {
    background-color: #6634e8;
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 100px rgb(47, 145, 235);
    margin-top: 100px;
}

form {
    max-width: 400px;
    margin: 0 auto;
}
</style>