<template>
    <section class="vh-100" style="background-color: #f46827;">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarTogglerDemo03"
                aria-controls="navbarTogglerDemo03" aria-expanded="false" aria-label="Toggle navigation">
                <i class="fas fa-bars"></i>
            </button>
            <a class="navbar-brand"><b>TicketShow</b></a>
            <a class="navbar-brand" style="color: yellow;"><b>UserDashboard</b></a>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                          <button @click="myprofile()" class="nav-link active"
                            style="color: rgb(0, 255, 17); background-color: rgb(37, 32, 32); border: none;" v-if="admin==0">MyProfile</button>
                    </li>
                    <li class="nav-item">
                        <button @click="logout" class="nav-link active"
                            style="color: #ff1515;background-color: rgb(37, 32, 32); border: none;">Logout</button>
                    </li>

                </ul>
                <form class="d- input-group " @submit.prevent="handleSearch">
                    <input v-model="searchTheatre" type="search" name="search" class="form-control" placeholder="Search Theatres"
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
                <h2 style="color:rgb(252, 252, 252)"><b>Current Theatre</b></h2>
                <br>

                <div class="col-3" v-for="theatre in theaters" :key="theatre.id">
                    <div class="p-3 border bg-light border-dark border-2">
                        <div class="col">

                            <div class="col">
                                <h6> <b>Theatre Name:</b> {{ theatre.name }}</h6>
                                <h6> <b>Location:</b> {{ theatre.location }}</h6>
                                <h6> <b>Place:</b> {{ theatre.place }}</h6>
                                <h6> <b>Capacity:</b> {{ theatre.capacity }}</h6>
                                
                            </div>

                            <br>
                            <div class="col">
                                <span><button class="btn btn-success" type="submit" @click="getshows(theatre.id)">Ongoing
                                        Shows</button></span>
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
    beforeMount() {
        this.getAllTheaters(); //calling the method to get details of all the theatres

    },
    data() {
        return {
            currentUser: '', // Set the current user name here
            searchTheatre:'',
            theaters: [],
            query:[],
            admin:'',
            user_id:''

        };
    },
    methods: {
        async getAllTheaters() {
            try {
                let access_token = localStorage.getItem('access_token');
                axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

                const response = await axios.get('http://localhost:8081/getalltheatre');
                this.theaters = response.data.theatre_list;
                this.admin = response.data.is_admin
                this.userid = response.data.user_id // Assuming the API response is an array of theaters
                console.log(this.theaters);
            } catch (error) {
                console.error(error);
            }
        },

        getshows(theatreId) {
            this.$router.push({ name: 'ongoingshows', params: { id: theatreId } })
        },
        async handleSearch(){
        try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        // console.log(formData)
        if (this.searchTheatre==''){
            this.getAllTheaters()
        }
        else{
        const response =  await axios.get('http://localhost:8081/search',{ params:{'Query':this.searchTheatre} })
        console.log(response)
        this.theaters = response.data.theatre; 
        }
      } catch (error) {
        console.log(error);
      }
            
        },
        myprofile(){
            this.$router.push({ name: 'myprofile', params: { id: this.userid } })
        },
        async logout() {
            try {
                localStorage.removeItem('access_token')
                localStorage.removeItem('username')

                alert('Successfully logged Out')
                this.$router.push('/')
            }

            catch (error) {
                console.log(error)
            }
        }
    }
};
</script>