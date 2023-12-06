<template>
    <section class="vh-100" style="background-color: #a00cf0;">
        <div class="container py-5 h-100">
            <div class="row d-flex justify-content-center align-items-center h-100">
                <div class="col col-xl-6">
                    <div class="card" style="border-radius: 1rem;">
                        <div class="row g-0">

                            <div class="col-md-6 col-lg-8 d-flex align-items-center">
                                <div class="card-body p-4 p-lg-5 text-black">

                                    <form @submit.prevent="submitForm">

                                        <div class="d-flex align-items-center mb-3 pb-1">
                                            <h1 class="fw-bold" style="text-align:center">TicketShow</h1>
                                        </div>

                                        <h5 class=" mb-3 pb-3" style="letter-spacing: 1px;">Welcome to AdminLogin Page</h5>

                                        <div class="form-outline mb-4">
                                            <input type="text" id="username" v-model="username"
                                                class="form-control form-control-lg" placeholder="Enter your Username"
                                                required />

                                        </div>

                                        <div class="form-outline mb-4">
                                            <input type="password" id="password" v-model="password"
                                                class="form-control form-control-lg" placeholder="Enter your Password"
                                                required />

                                        </div>

                                        <div class="pt-1 mb-4">
                                            <button class="btn btn-dark btn-lg btn-block" type="submit">Login</button>
                                        </div>

                                    </form>
                                    
                                    <p style="color: #040404;">Already have an User Account ? <RouterLink to="/"
                                            style="color: #ff0000;">Click Here</RouterLink></p>


                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import axios from 'axios';
export default{
    data(){
        return {
            username:'',
            password:''
        };
    },
    methods:{
        async submitForm(){
            //getting the usename and password entered by the user from the form
            const formData = {
                username: this.username,
                password: this.password
            };
            // Perform login logic here 
            // Can make an API request or perform any other necessary actions
            // Make an API request to your Flask backened
            // Make an API request to your Flask backened
            //sending a post request to login route in the api with the user credentials
            axios.post('http://localhost:8081/login',formData).then(response => {
                // Handle successfull login response
                if (response.data.status === 'success'){ 
                    //on successfull match of the credentials, access token,referesh token and username are stored in localStorage
                    const access_token = response.data.access_token;
                    const refresh_token = response.data.refresh_token;
                    const username = response.data.username;
                // Store the token in local storage or vuex store for future use 
                    localStorage.setItem('access_token',access_token);
                    localStorage.setItem('refresh_token',refresh_token);
                    localStorage.setItem('username',username);

                    alert('Successfully logged in')
                       this.$router.push('/admin/dashboard');
            }
            else
            {
                alert('Invalid Credentials')
            }
        })
            .catch(error => {
                // Handle login error
                console.error(error);
                alert('Login Failed. Please check your credentials and try again.');
            });
            this.username = '';
            this.password = '';
        }
    }
}
</script>