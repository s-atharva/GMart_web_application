<template>
    <div class="header-container">
        <div>
            <h1 class="page-header">Hello {{ user.username }}</h1>
        </div>
        <div class="search-input">
            <input v-model="searchQuery" class="form-control mr-sm-2" type="search" placeholder="Search Categories">
        </div>
        <div class="navigation">
            <router-link to="/home" class="btn btn-primary mr-2">Home</router-link>
            <router-link to="/cart" class="btn btn-secondary mr-2">Cart</router-link>
            <router-link to="/orders" class="btn btn-secondary mr-2">Orders</router-link>
            <button @click="logout" class="btn btn-success">Logout</button>
        </div>

    </div>
    <div v-if="categories.length > 0" class="container-home">
        <h1 class="section-title">Categories</h1>
        <div v-for="category in categories" :key="category.categoryId" class="card"
             style="width: 18rem;">
            <router-link
                :to="{ name: 'CustomerProductsPage', params: { categoryId: category.categoryId, categoryName: category.name } }">
                <img class="card-img-top" :src="category.image_path" alt="Card image cap"
                     style="width: 100%; height: 150px; object-fit: cover">
                <div class="card-body">
                    <h5 class="card-title">{{ category.name }}</h5>

                    <p class="card-text">{{ category.description }}</p>
                </div>
            </router-link>
        </div>
    </div>
    <div v-else>
        <h2>No Category</h2>
    </div>

</template>

<script>
import axios from "axios";

export default {
    name: 'CustomerHomePage',
    data() {
        return {
            categories: [],
            searchQuery: ''
        }
    },
    mounted() {
        this.getCategories();
    },
    watch: {
        searchQuery: 'getCategories'
    },
    methods: {
        logout() {
            // Clear user information from session storage
            sessionStorage.removeItem('user');
            // Redirect to the login page
            this.$router.replace('/customer/login')
        },
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
                    if (this.searchQuery) {
                        const searchRegex = new RegExp(this.searchQuery, 'i');
                        this.categories = this.categories.filter(category => searchRegex.test(category.name));
                    }
                    console.log(this.categories)
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                })
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
.container-home {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(80vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 3.5rem 16px 16px;
    margin-top: 10%;
    margin-left: 10%;
    border: 2px solid #ffffff;
    box-sizing: border-box;
    width: 80%;
}

.page-header {
    color: #ffffff;
}

.search-input {
    width: 25%;
    padding: 15px;
    font-size: 16px;
    margin-bottom: 10px;
}
</style>