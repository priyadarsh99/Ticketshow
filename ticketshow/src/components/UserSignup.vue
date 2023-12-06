<template>
    <section class="vh-150" style="background-color: #ee290b;">
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

                                        <h5 class=" mb-3 pb-3" style="letter-spacing: 1px;">Welcome to UserSignUp Page</h5>

                                        <div class="form-outline mb-4">
                                            <input type="text" id="username" v-model="username"
                                                class="form-control form-control-lg" placeholder="Enter your Username"
                                                required />

                                        </div>

                                        <div class="form-outline mb-4">
                                            <input type="email" id="email" v-model="email"
                                                class="form-control form-control-lg" placeholder="Enter your Email"
                                                required />

                                        </div>

                                        <div class="form-outline mb-4">
                                            <input type="password" id="password" v-model="password"
                                                class="form-control form-control-lg" placeholder="Enter your Password"
                                                required />

                                        </div>

                                        <div class="form-outline mb-4">
                                            <input type="password" id="confirm-password" v-model="confirmPassword"
                                                class="form-control form-control-lg" placeholder="Confirm your Password"
                                                required />

                                        </div>

                                        <div class="pt-1 mb-4">
                                            <button class="btn btn-dark btn-lg btn-block" type="submit">SignUp</button>
                                        </div>

                                    </form>
                                    <p style="color: #040404;">Already have an Admin Account? <RouterLink to="/adminlogin"
                                            style="color: #ff0000;">Login here</RouterLink></p>
                                    <p style="color: #040404;">Already have an User Account ? <RouterLink to="/"
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
import axios from "axios";
export default{
    data(){
        return {
            username: "",
            password: "",
            email:"",
            confirmPassword: ""
        };
    },
    methods: {
        submitForm(){
            const formData = {
                //taking the credentials of the new user
                username : this.username,
                password : this.password,
                email: this.email
            };
            
            if (this.password !== this.confirmPassword){
                alert("Passwords Do not Match");
                return;
            }

            // Performing Signup logic here
            // YOu can make an API request or perform any other necessary actions
            axios.post('http://localhost:8081/api/usersignup', formData).then(response =>{
                //Handle successfull login response 
                alert(response.data.message)

                // Redirect to the desired user page
                this.$router.push('/');
            }).catch(error => {
                // handle login error
                console.error(error);
                alert(error);
            });

            // Reset form fields 
            this.username = "";
            this.password = "";
            this.email = "",
            this.confirmPassword = "";
            
        }
    }
}

</script>