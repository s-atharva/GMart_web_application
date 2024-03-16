<template>
    <div class="updateCategory">
        <h1>Update Category</h1>
        <br>
        <form @submit.prevent="updateCategory">
            <p>Category Id {{ this.categoryId }}</p>
            <div class="form-group">
                <label for="categoryName">Category Name</label>
                <input v-model="categoryName" type="text" class="form-control" id="categoryName" required>
            </div>

            <div class="form-group">
                <label for="categoryName">Description</label>
                <input v-model="categoryDescription" type="text" class="form-control" id="categoryName" required>
            </div>

            <div class="form-group">
                <label for="categoryName">Image Path</label>
                <input v-model="imagePath" type="text" class="form-control" id="categoryName" required>
            </div>

            <button type="submit" class="btn btn-success">Update</button>
        </form>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'UpdateCategory',
    data() {
        return {
            categoryId: '',
            categoryName: '',
            categoryDescription: '',
            imagePath: ''
        }
    },
    created() {
        this.categoryId = this.$route.params.categoryId
    },
    methods: {
        updateCategory() {
            console.log(this.categoryName, this.categoryDescription)
            const data = {
                name: this.categoryName,
                description: this.categoryDescription,
                image_path: this.imagePath
            }
            axios.put(`http://127.0.0.1:8005/categories/${this.categoryId}`, data, {headers: {"Authorization": `Bearer ${this.user.access_token}`}})
                .then(response => {
                    console.log('Category updated successfully:', response.data)
                    this.$router.push('/categories')

                })
                .catch(error => {
                    console.error('Error updating category:', error);
                })
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

.updateCategory {
    background-color: #4955fa;
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    margin-top: -20px;
}

form {
    max-width: 400px;
    margin: 0 auto;
}
</style>