<template>
    <section class="vh-100" style="background-color: #0cc6f0;">
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

                                        <h5 class=" mb-3 pb-3" style="letter-spacing: 1px;">Welcome to UserLogin Page</h5>

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
                                    <p style="color: #040404;">Don't have an User Account? <RouterLink to="/usersignup"
                                            style="color: #ff0000;">Signup here</RouterLink></p>
                                    <p style="color: #040404;">Already have an Admin Account ? <RouterLink to="/adminlogin"
                                            style="color: #ff0000;">Login Here</RouterLink></p>


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
            //method which takes the user credentials entered by the user and checks whether they are correct or not
            const formData = {
                username: this.username,
                password: this.password
            };
            // Perform login logic here 
            // Can make an API request or perform any other necessary actions
            // Make an API request to your Flask backened
            // Make an API request to your Flask backened

            axios.post('http://localhost:8081/login',formData).then(response => {
                // Handle successfull login response 

                if (response.data.status ==='success')
                {   //when the credentials are correct
                    const access_token = response.data.access_token; //storing the access token
                    const refresh_token = response.data.refresh_token; //storing the refresh token
                    const username = response.data.username; // storing the username of the user
                    const isAdmin = response.data.is_admin; //storing whether the user is admin/normaluser
                // Store the token in local storage or vuex store for future use 
                    localStorage.setItem('access_token',access_token);
                    localStorage.setItem('refresh_token',refresh_token);
                    localStorage.setItem('username',username);
                    localStorage.setItem('isAdmin',isAdmin);

                    alert('Successfully user logged in')
                    this.$router.push('/user/dashboard');
                    
                }
                else{
                    alert('Invalid Credentials')
                }
            }).catch(error => {
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