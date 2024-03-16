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


    <div class="container-manager-box">
        <div v-for="category in categories" :key="category.categoryId" class="card" style="width: 18rem">
            <router-link
                :to="{name: 'CategoryProducts', params: {categoryId : category.categoryId, categoryName : category.name}}">
                <img class="card-img" :src="category.image_path"
                     style="width: 100%; height: 150px; object-fit: cover">
            </router-link>
            <div class="card-body">
                <h5 class="card-title">Name: {{ category.name }}</h5>
                <p class="card-description">Description: {{ category.description }}</p>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'ManagerDashBoard',
    data() {
        return {
            categories: []
        }
    },
    mounted() {
        this.getCategories()
    }
    ,
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
                    console.error("Error fetching categories", error)
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

.header-container-manager {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 2px;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background-color: #037794; /* Optional: Set a background color if needed */
    z-index: 1000; /* Ensure the header is above other elements */
}

.container-manager-box {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 15%;
    margin-right: 13%;
    border: 2px solid #ffffff;
    box-sizing: border-box;
    //box-shadow: 0 0 50px rgba(224, 179, 179, 0.5);
    width: 100%;
}
</style>