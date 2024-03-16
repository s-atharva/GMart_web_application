<template>
    <div class="login">
        <h1>Admin Login</h1>
        <form v-on:submit.prevent="login">
            <div class="form-group">
                <label for="username">User Name</label>
                <input type="text" class="form-control" id="username" v-model="userName" required>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <br>

        <p v-if="message">{{ message }}</p>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'AdminLoginPage',
    data() {
        return {
            userName: '',
            password: '',
            message: '',
        }
    },
    methods: {
        login() {
            const url = 'http://127.0.0.1:8005/login'
            const data = {
                userName: this.userName,
                password: this.password,
                role: 'ADMIN'
            }
            axios.post(url, data)
                .then(response => {
                    this.message = response.data.message
                    this.userID = response.data.user_id

                    if (response.data.success) {
                        sessionStorage.setItem('user', JSON.stringify(response.data))
                        this.$router.push('/categories')
                    }
                })
                .catch(error => {
                    this.message = error.response.data.message
                })
        }
    }
}
</script>


<style scoped>
body {
    background-color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 75vh;
    margin: 0;
}

.login {
    background-color: #6634e8;
    color: white;
    padding: 100px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
//margin-top: 10px; ////margin-bottom: 10px;
}

form {
    max-width: 400px;
    margin: 0 auto;

}
</style>