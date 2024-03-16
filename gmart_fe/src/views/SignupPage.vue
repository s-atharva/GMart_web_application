<template>
    <div>
        <br>
        <nav>
            <router-link to="/customer/login">Login</router-link>
            |
            <router-link to="/customer/signup">SignUp</router-link>
        </nav>
    </div>

    <div class="signup">
        <h1>SignUp</h1>
        <br>
        <form v-on:submit.prevent="addCustomer">
            <div class="form-group">
                <label for="firstName">First Name</label>
                <input type="text" class="form-control" id="firstName" v-model="firstName" required>
            </div>
            <div class="form-group">
                <label for="lastName">Last Name</label>
                <input type="text" class="form-control" id="lastName" v-model="lastName" required>
            </div>
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" class="form-control" id="username" v-model="userName" required>
            </div>
            <div class="form-group">
                <label for="email">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
            <div class="form-group">
                <label for="password">password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-success">SignUp</button>
        </form>
    </div>
</template>

<script>
// @ is an alias to /src
import axios from "axios";

export default {
    name: 'SignupPage',
    data() {
        return {
            firstName: '',
            lastName: '',
            userName: '',
            email: '',
            password: ''
        }
    },
    methods: {
        async addCustomer() {
            const result = await axios.post('http://127.0.0.1:8005/user', {
                first_name: this.firstName,
                last_name: this.lastName,
                username: this.userName,
                email: this.email,
                password: this.password,
                role: 'CUSTOMER',
            })
            // console.log("Function called", this.firstName, this.lastName, this.userName, this.email, this.password)
            console.warn(result)
            this.$router.push('/customer/login')
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

.signup {
    background-color: #247be4;
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