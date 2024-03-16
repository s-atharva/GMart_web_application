<template>
    <div class="page-container">
        <div class="header-container-admin">
            <div>
                <h1 v-if="user" class="page-header">Hello {{ user.username }} </h1>
            </div>
            <div class="navigation">
                <router-link to="/categories" class="btn btn-primary mr-2">Home</router-link>
                <router-link to="/categories/add" class="btn btn-primary mr-2">Add Category</router-link>
                <router-link to="/categories/requested" class="btn btn-secondary mr-2">Requested Categories
                </router-link>
                <button @click="logout" class="btn btn-success">Logout</button>
            </div>
        </div>
        <div class="scrollable-box-admin">
            <div v-for="category in categories" :key="category.categoryId" class="card" style="width: 18rem;">
                <img class="card-img-top" :src="category.image_path" alt="Card image cap"
                     style="width: 100%; height: 150px; object-fit: cover">
                <div class="card-body">
                    <h5 class="card-title">{{ category.name }}</h5>

                    <p class="card-text">{{ category.description }}</p>
                    <router-link
                        :to="{ name: 'updateCategory', params: { categoryId: category.categoryId } }"
                        class="btn btn-primary mr-2">Update
                    </router-link>
                    <a @click="deleteCategory(category.categoryId)" class="btn btn-danger">Delete</a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'CategoriesPage',
    data() {
        return {
            categories: []
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
        deleteCategory(categoryId) {
            axios.delete(`http://127.0.0.1:8005/categories/delete/${categoryId}`, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    if (response.data.success) {
                        // If deletion is successful, update the categories list
                        this.getCategories();
                    } else {
                        console.error('Error deleting category:', response.data.message);
                    }
                })
                .catch(error => {
                    console.error('Error deleting category:', error);
                });

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
.card {
    margin: 10px;
}

.header-container-admin {
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

.scrollable-box-admin {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    overflow: auto;
    max-height: calc(90vh - 2 * 16px - 5.5rem); /* Adjusted max-height */
    padding: 0.5rem 16px 16px;
    margin-top: 30%;
    margin-left: -150%;
    width: 400%;

}

.item-divider {
    border: 5px solid #e85b5b;
    margin: 10px 0;
}

</style>