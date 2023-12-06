<template>
    <section class="vh-180" style="background-color: #af00fa;">
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
                            <h1 class="fw-bold" style="text-align:center" >UpdateShow</h1>
                          </div>
        
                          <h5 class=" mb-3 pb-3" style="letter-spacing: 1px;">Please Enter the Show Details </h5>
        
                          <div class="form-outline mb-4">
                            <input type="text" id="showname" v-model="showname"
                                                class="form-control form-control-lg" placeholder="Enter Name of Show"
                                                disabled readonly />
                            
                          </div>
        
                          <div class="form-outline mb-4">
                            <input type="text" id = "rating" v-model="rating" class="form-control form-control-lg" placeholder="Enter Rating of Show" required/>
                            
                          </div>
                          
                          <div class="form-outline mb-4">
                            <input type="text" id = "timing" v-model="time" class="form-control form-control-lg" placeholder="Enter Time of Show" required/>
                            
                          </div>
                          
                          <div class="form-outline mb-4">
                            <input type="text" id = "tags" v-model="tags" class="form-control form-control-lg" placeholder="Enter Tags" required/>
                            
                          </div>
                          
                          <div class="form-outline mb-4">
                            <input type="text" id = "price" v-model="price" class="form-control form-control-lg" placeholder="Enter Price" required/>
                            
                          </div>

                          <!-- <div class="form-outline mb-4">
                            <input type="file" name = "photo" id="form2Example27" class="form-control form-control-lg" required/>
                            
                          </div> -->

                          <div class="pt-1 mb-4">
                            <button class="btn btn-dark btn-lg btn-block" type="submit">Update Show</button>
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
        showId: '', // ID of the show to be updated
        showName:'',
        rating: null,
        time: '',
        tags: '',
        price: null,
      };
    },
    created() {
    // Fetch the theater data or receive it as a prop
    this.showId = this.$route.params.id; // Assuming the show ID is passed via route params
    console.log(this.showId)
    // Perform API request to fetch show data
    this.fetchshow();
    },
    methods: {
      async fetchshow() {
        //method which first gets the show data from the database whose details have to be updated
      try {

        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        //calling the editshow route of the api with the show id whose details are needed
        const response = await axios.get('http://localhost:8081/editshow',{
          params:{
            id:this.showId
          }
        });
        const showData = response.data.show; 
        console.log(showData)
        // 
        this.showName = showData.showname;
        this.rating = showData.ratings;
        this.tags = showData.tags;
        this.price = showData.price;
        this.time = showData.time;
      } catch (error) {
        console.error('Error fetching show data:', error);
      }
    },
      submitForm() {
        //method which takes the updated details of the show and makes changes in the database
        // Perform create theatre logic here
        const formData = {
                id:this.showId,
                rating: this.rating,
                tags:this.tags,
                price:this.price,
                time:this.time,
            };

            let access_token = localStorage.getItem('access_token');

            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

            // You can make an API request or perform any other necessary actions
            axios.put('http://localhost:8081/editshow', formData)
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
        this.showName = '';
        this.tags = '';
        this.rating = null;
        this.price = null;
        this.time = ''
      },
    }
  };
  </script>