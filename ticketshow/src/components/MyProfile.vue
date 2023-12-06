<template>
    <section class="vh-100" style="background-color: #f007dd;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
                    data-mdb-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                </button>
                <a class="navbar-brand" ><b>TicketShow</b></a>
                <a class="navbar-brand" style="color: yellow;"><b>ProfilePage</b></a>
                <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        
                        <li class="nav-item">
                            <button @click="logout" class="nav-link active" style="color: #ff1515; background-color: rgb(37, 32, 32); border: none;">Logout</button>
                        </li>

                    </ul>

                </div>

                
            </div>
        </nav>
    

    <section class="gradient-custom">
            <div class="container">
                <div class="row g-3">
                    <h1></h1>
                    <h2 style="color:rgb(252, 253, 251)"><b>My Bookings</b></h2>
                    <div class="col-3" v-for="show in shows" :key="show.id">
                        <div class="p-3 border bg-light border-dark border-2">
                            <div class="col">
                            
                                <div class="col">
                                    <h6 > <b>Show Name:</b> {{ show.showname }}</h6>
                                
                                    <h6> <b>Ratings:</b> {{ show.ratings }}</h6>

                                    <h6> <b>Tags:</b> {{ show.tags }}</h6>
                                    <h6> <b>Price:</b> ₹{{ show.price }}</h6>
                                    <h6> <b>Time:</b> {{ show.time }}</h6>
                                    
                                </div>

                                <br>
                                <div class="col" >
                                    <span><button  class="btn btn-warning" type="submit" @click="rateShow(show.id)">Rate Show</button></span>
                                    <br>
                                </div>
                                                                
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
      </section>
</template>


<script>
  import axios from "axios";
  export default {
    beforeMount(){
      this.myprofile();
      
    },
    data() {
      return {
        
        shows: [],
        userid:'',
        
      };
    },
    created() {
    // Fetch the theater data or receive it as a prop
    this.userid = this.$route.params.id; // Assuming the theater ID is passed via route params

    // Perform API request to fetch theater data
    this.myprofile();
    },
    methods: {
      //method which is used to get information about a particular user
      async myprofile() {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        console.log('GET SHOWS')
        //calling the myprofile route of the api with the id of the user whose details are needed
        const response = await axios.get('http://localhost:8081/myprofile',{
          params:{
            id:this.userid
          }
        })
        this.shows = response.data.show_list;  //storing the details of the shows booked by the respective user
        console.log(this.userid)
        console.log(this.shows);
        
      } catch (error) {
        console.error(error);
      }
    },
    rateShow(showId){
      // method which calls the rateshow route with the id of the show whose rating has to be submitted
        this.$router.push({ name: 'rateshow', params: { id: showId } });
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
    },

    }
  };
  </script>