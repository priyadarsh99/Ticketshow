<template>
    <section class="vh-180" style="background-color: #fa9e00;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
                    data-mdb-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                </button>
                <a class="navbar-brand" ><b>TicketShow</b></a>
                <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <RouterLink to="/adminlogin" class="nav-link active" style="color: #ff0000;">Logout</RouterLink>
                        </li>

                    </ul>

                </div>
            </div>
        </nav>

        <div class="container py-5 h-200">
            <div class="row d-flex justify-content-center align-items-center h-100">
              <div class="col col-xl-6">
                <div class="card" style="border-radius: 1rem;">
                  <div class="row g-0">
  
                    <div class="col-md-6 col-lg-8 d-flex align-items-center">
                      <div class="card-body p-4 p-lg-5 text-black">
        
                      <form @submit.prevent="submitForm" >
        
                          <div class="d-flex align-items-center mb-3 pb-1" >
                            <h1 class="fw-bold" style="text-align:center" >CreateTheatre</h1>
                          </div>
        
                          <h5 class=" mb-3 pb-3" style="letter-spacing: 1px;">Please Enter the Theatre Details </h5>
        
                          <div class="form-outline mb-4">
                            <input type="text" id="theatrename" v-model="theatrename"
                                                class="form-control form-control-lg" placeholder="Enter Name of Theatre"
                                                required />
                            
                          </div>
        
                          <div class="form-outline mb-4">
                            <input type="text" id = "place" v-model="place" class="form-control form-control-lg" placeholder="Enter Name of Place" required/>
                            
                          </div>
                          
                          <div class="form-outline mb-4">
                            <input type="text" id = "location" v-model="location" class="form-control form-control-lg" placeholder="Enter Name of Location" required/>
                            
                          </div>
                          
                          <div class="form-outline mb-4">
                            <input type="text" id = "capacity" v-model="capacity" class="form-control form-control-lg" placeholder="Enter Capacity of Theatre" required/>
                            
                          </div>
                          

                          <!-- <div class="form-outline mb-4">
                            <input type="file" name = "photo" id="form2Example27" class="form-control form-control-lg" required/>
                            
                          </div> -->

                          <div class="pt-1 mb-4">
                            <button class="btn btn-dark btn-lg btn-block" type="submit">Create Theatre</button>
                          </div>
        
                      </form>
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
  export default {
    data() {
      return {
        theatrename: '',
        place: '',
        location: '',
        capacity: null
      };
    },
    methods: {
      submitForm() {
        // Perform create theatre logic here
        //stores the information of the new theater via the form
        const formData = {
                theatrename: this.theatrename,
                place: this.place,
                location:this.location,
                capacity:this.capacity
            };

            let access_token = localStorage.getItem('access_token');

            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

            // You can make an API request or perform any other necessary actions
            //calling the createtheatre route of the api with the details of the theatre to be created
            axios.post('http://localhost:8081/createtheatre', formData)
              .then(response => {
              // Handle successful login response
              alert(response.data.message);
              // Redirect to the desired admin page
              this.$router.push('/admin/dashboard');
            })
            .catch(error => {
            // Handle login error
            console.error(error);
            alert(error);
            });
  
        // Reset form fields
        this.theatrename = '';
        this.place = '';
        this.location = '';
        this.capacity = null;
      }
    }
  };
  </script>