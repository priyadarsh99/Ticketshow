<template>
    <section class="vh-100" style="background-color: #3df0c6;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
                    data-mdb-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                </button>
                <a class="navbar-brand" ><b>TicketShow</b></a>
                <a class="navbar-brand" style="color: yellow;" ><b>CurrentShows</b></a>
                <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                          <button @click="myprofile()" class="nav-link active"
                            style="color: rgb(0, 255, 17); background-color: rgb(37, 32, 32); border: none;" v-if="admin==0">MyProfile</button>
                        </li>

                        <li class="nav-item" v-if="admin==1">
                            <button @click="createshow" class="nav-link active" style="color: rgb(0, 255, 17);background-color: rgb(37, 32, 32); border: none;">CreateShow</button>
                        </li>
                        <li class="nav-item" v-if="admin==1">
                            <button @click="summary" class="nav-link active" style="color: rgb(238, 242, 238); background-color: rgb(37, 32, 32); border: none;">Summary</button>
                        </li>
                        <li class="nav-item">
                            <button @click="logout" class="nav-link active" style="color: #ff1515; background-color: rgb(37, 32, 32); border: none;">Logout</button>
                        </li>

                    </ul>
                    <form class="d- input-group " @submit.prevent="handleSearch">
                    <input v-model="searchShows" type="search" name="search" class="form-control" placeholder="Search Shows"
                        aria-label="Search" />
                    <button class="btn btn-outline-primary" type="submit" data-mdb-ripple-color="dark">
                        Search
                    </button>
                </form>
                </div>
            </div>
        </nav>
    

    <section class="gradient-custom">
            <div class="container">
                <div class="row g-3">
                    <h1></h1>
                    <h2 style="color:rgb(19, 10, 17); text-align:center"><b>Current Shows</b></h2>
                    <br>
                    <div class="col-3" v-for="show in shows" :key="show.id">
                        <div class="p-3 border bg-light border-dark border-2">
                            <div class="col">
                            
                                <div class="col">
                                    <h6> <b>Place of Theatre: </b> {{ show.theatre }}</h6>

                                    <h6 > <b>Location:</b> {{ show.location }}</h6>

                                    <h6 > <b>Show Name:</b> {{ show.showname }}</h6>
                                
                                    <h6> <b>Ratings:</b> {{ show.ratings }}</h6>

                                    <h6> <b>Tags:</b> {{ show.tags }}</h6>
                                    <h6> <b>Price:</b> ₹{{ show.price }}</h6>
                                    <h6> <b>Time:</b> {{ show.time }}</h6>
                                    <h6> <b>Available Capacity: </b> {{show.capacity }}</h6>
                                    
                                </div>

                                <br>
                                <div class="col" v-if="admin==0"  >
                                    <div class="col" v-if="show.capacity!=0">
                                    <span><button  class="btn btn-warning" type="submit" @click="bookShow(show.id)">Book Show</button></span>
                                    <br>
                                    </div>
                                    <div class="col" v-if="show.capacity==0">
                                    <span><button  class="btn btn-danger" disabled>Housefull</button></span>
                                    <br>
                                    </div>
                                </div>
                                <br>
                                <div class="col" v-if="admin==1">
                                    <span><button class="btn btn-primary" type="submit" @click="updateShow(show.id)">Update Show</button></span>
                                </div>
                                <br>
                                <div class="col" v-if="admin==1">
                                    <span><button  class="btn btn-danger" type="submit" @click="deleteShow(show.id)">Delete Show</button></span>
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
      this.getshows(); //calling the getshows method to fetch the currently running shows
      
    },
    data() {
      return {
        theatreId: '', // Set the current user name here
        shows: [],
        admin:'',
        userid:'',
        searchShows:'',
        

      };
    },
    created() {
    // Fetch the theater data or receive it as a prop
    this.theatreId = this.$route.params.id; // Assuming the theater ID is passed via route params

    // Perform API request to fetch theater data
    this.getshows();
    },
    methods: {
      async getshows() {
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        console.log('GET SHOWS')
        const response = await axios.get('http://localhost:8081/getshows',{
          params:{
            id:this.theatreId
          }
        })
        this.shows = response.data.show_list; 
        this.admin = response.data.is_admin// Assuming the API response is an array of theaters
        this.userid = response.data.user_id
      
        console.log(this.shows);
        console.log(this.admin);
      } catch (error) {
        console.error(error);
      }
    },
    async handleSearch(){
        // method which is used when user searches something via the search bar
        try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        // console.log(formData)
        if (this.searchShows==''){
          //whenever the search bar is empty , the currently running shows will be displayed
            this.getshows()
            
        }
        else{
          //calling the searchshows route of the api with the search query of the user
        console.log(this.searchShows)
        console.log(this.theatreId)
        const response =  await axios.get('http://localhost:8081/searchshows',{ params:{'Query':this.searchShows,'id':this.theatreId} })
        console.log(response)
        this.shows = response.data.shows; 
        // this.avai_capacity()
        }
      } catch (error) {
        console.log(error);
      }
            
        },
      
    createshow() {
        // Perform logic to add a venue here
        this.$router.push({ name: 'createshow', params: { id: this.theatreId } });
    },
    
    updateShow(showId){
        this.$router.push({name: 'updateshow', params:{id:showId}})
    },
    bookShow(showId) {
        // Perform logic to add a venue here
        this.$router.push({ name: 'bookshow', params: { id: showId } });
    },
    async deleteShow(showId) {
      const confirmDelete = window.confirm('Are you sure you want to delete this show?');
      if (!confirmDelete) {
        return; // Admin cancelled the deletion
      }

      try {
        const formData = {
          id: showId
        };
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = await axios.delete('http://localhost:8081/editshow', {
          data: formData
        });
        alert(response.data.message);
        this.shows = this.shows.filter(show => show.id !== showId);
      } catch (error) {
        console.error(error);
        alert(response.data.message);
      }
    },
    myprofile(){
      this.$router.push({ name: 'myprofile', params: { id: this.userid } })
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