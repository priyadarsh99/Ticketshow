<template>
    <section class="vh-100" style="background-color: #003efa;">
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
                            <h1 class="fw-bold" style="text-align:center" >BookShow</h1>
                          </div>
        
                          <h5 class=" mb-3 pb-3" style="letter-spacing: 1px;">Please Enter the No. of Ticket to Book </h5>
        
                          <div class="form-outline mb-4">
                            <input type="text" id="count" v-model="count"
                                                class="form-control form-control-lg" placeholder="Enter No. of Tickets"
                                                required />
                            
                          </div>

                          <div class="pt-1 mb-4">
                            <button class="btn btn-dark btn-lg btn-block" type="submit">Book Show</button>
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
    beforeMount(){
      this.getshows();
    },
    data() {
      return {
        showId: '', // Set the current user name here
        shows: [],
        count:null,
        user_id:null,
      };
    },
    created() {
    // Fetch the theater data or receive it as a prop
    this.showId = this.$route.params.id; // Assuming the show ID is passed via route params

    // Perform API request to fetch theater data
    this.getshows();
    },
    methods: {
      async getshows() {
        //method to get the shows details
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        console.log('GET SHOWS')
        //sending the get request to the editshow api 
        const response = await axios.get('http://localhost:8081/editshow',{
          params:{
            id:this.showId
          }
        })
        this.shows = response.data.show; 
        this.user_id = response.data.user_id;
        console.log(this.shows);
        
      } catch (error) {
        console.error(error);
      }
    },
    submitForm(){
      //method which is used to book a particular show
        const formData = {
          //stores the data of the show to be booked
                show_id: this.shows.id,
                theatre_id:this.shows.theatre_id,
                count: this.count, //no. of tickets to be booked
                user_id: this.user_id
            };
            console.log(formData)
            let access_token = localStorage.getItem('access_token');
            axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

            axios.post('http://localhost:8081/bookshow', formData)
              .then(response => {
              // Handle successful login response
              alert(response.data.message);
              // Redirect to the desired admin page
              history.back();
            })
            .catch(error => {
            // Handle login error
            console.error(error);
            alert(error);
            });
      },
    async logout(){
        try{
            localStorage.removeItem('access_token')
            localStorage.removeItem('username')

            alert('Successfully logged Out')
            this.$router.push('/')
        }

        catch(error){
            console.log(error)
        }
    }
    }
  };
  </script>