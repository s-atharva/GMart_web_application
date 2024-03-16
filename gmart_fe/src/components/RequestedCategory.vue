<template>
    <div class="header-container-admin">
        <div>
            <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
        </div>
        <div class="navigation">
            <router-link to="/categories" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/categories/add" class="btn btn-primary mr-2">Add Category</router-link>
            <router-link to="/categories" class="btn btn-secondary">Back to Categories</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>
    </div>

    <div v-if="categories.length === 0">
        <h3>No Requested Category</h3>
    </div>
    <div v-else class="container-requested">
        <div v-for="category in categories" :key="category.categoryId" class="card" style="width: 18rem;">
            <img class="card-img-top" :src="category.image_path" alt="Card image cap"
                 style="width: 100%; height: 150px; object-fit: cover">
            <div class="card-body">
                <h5 class="card-title">{{ category.name }}</h5>

                <p class="card-text">{{ category.description }}</p>
                <button @click="approveCategory(category.categoryId)" class="btn btn-success mr-2">Approve</button>
                <button @click="rejectCategory(category.categoryId)" class="btn btn-danger">Reject</button>
            </div>

        </div>

    </div>
</template>

<script>
import axios from "axios";

export default {
    name: "RequestedCategory",
    data() {
        return {
            categories: []
        }
    },
    mounted() {
        this.getRequestedCategories()
    },
    methods: {
        getRequestedCategories() {
            axios.get('http://127.0.0.1:8005/categories/requested', {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
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
        },
        approveCategory(categoryId) {
            const data = {
                status: 'ACTIVE'
            }
            console.log(data)
            axios.put(`http://127.0.0.1:8005/categories/${categoryId}`, data, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log("Category approved successfully", response.data)
                    this.getRequestedCategories()
                })
                .catch(error => {
                    console.error('Error in Approving category:', error);
                })
        },
        rejectCategory(categoryId) {
            const data = {
                status: 'REJECTED'
            }
            console.log(data)
            axios.put(`http://127.0.0.1:8005/categories/${categoryId}`, data, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log("Category rejected successfully", response.data)
                    this.getRequestedCategories()
                })
                .catch(error => {
                    console.error('Error in Approving category:', error);
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
.container-requested {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 30%;
    border: 2px solid #ffffff;
    box-sizing: border-box;
    width: 100%;
}
</style>