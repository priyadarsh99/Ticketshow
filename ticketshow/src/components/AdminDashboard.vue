<template>
    <section class="vh-100" style="background-color: #9d00fe;">
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <button class="navbar-toggler" type="button" data-mdb-toggle="collapse"
                    data-mdb-target="#navbarTogglerDemo03" aria-controls="navbarTogglerDemo03" aria-expanded="false"
                    aria-label="Toggle navigation">
                    <i class="fas fa-bars"></i>
                </button>
                <a class="navbar-brand" ><b>TicketShow</b></a>
                <a class="navbar-brand" style="color: yellow;"><b>AdminDashboard</b></a>
                <div class="collapse navbar-collapse" id="navbarTogglerDemo03">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item">
                            <button @click="addTheatre" class="nav-link active" style="color: rgb(0, 255, 17);  background-color: rgb(37, 32, 32); border: none;">CreateTheatre</button>
                        </li>
                        <li class="nav-item">
                            <button @click="summary" class="nav-link active" style="color: rgb(236, 238, 239);  background-color: rgb(37, 32, 32); border: none;">Summary</button>
                        </li>
                        <li class="nav-item">
                            <button @click="logout" class="nav-link active" style="color: #ff1515; background-color: rgb(37, 32, 32); border: none;">Logout</button>
                        </li>

                    </ul>
                </div>
            </div>
        </nav>
    

    <section class="gradient-custom">
            <div class="container" >
                <div class="row g-3">
                    <h1></h1>
                    <h2 style="color:rgb(252, 252, 252); text-align:center"><b>Current Theatres</b></h2>
                    <br>
                
                    <div class="col-3" v-for="theatre in theaters" :key="theatre.id" >
                        <div class="p-3 border bg-light border-dark border-2" >
                            <div class="col" >
                            
                                <div class="col" >
                                    <h6 > <b>Theatre Name:</b> {{ theatre.name }}</h6> 
                                    <h6> <b>Location:</b> {{ theatre.location }}</h6>
                                    <h6> <b>Place:</b> {{ theatre.place }}</h6>
                                    <h6> <b>Capacity:</b> {{ theatre.capacity }}</h6>
                                </div>

                                <br>
                                <div class="col">
                                    <span><button  class="btn btn-warning" type="submit" @click="createshow(theatre.id)">Create Show</button></span>
                                </div>
                                <br>
                                <div class="col">
                                    <span><button  class="btn btn-success" type="submit" @click="getshows(theatre.id)">Ongoing Shows</button></span>
                                </div>
                                <br>
                                <div class="col">
                                    <span><button  class="btn btn-danger" type="submit" @click="deleteTheatre(theatre.id)">Delete Theatre</button></span>
                                </div>
                                <br>
                                <div class="col">
                                    <span><button class="btn btn-primary" type="submit" @click="updateTheatre(theatre.id)">Update Theatre</button></span>
                                </div>
                                <br>
                                <div class="col">
                                    <span><button class="btn btn-dark" type="submit" @click="exportTheatre(theatre.id)">Export Theatre</button></span>
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
      this.getAllTheaters(); //calling the getalltheatres method before mount
    },
    data() {
      return {
        currentUser: '', // Set the current user name here
        theaters: []
      };
    },
    methods: {
      async getAllTheaters() {
      try {
        //method which is used to get all the theatres details
        let access_token = localStorage.getItem('access_token'); // getting the access token
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = await axios.get('http://localhost:8081/getalltheatre'); //sending get request to api
        this.theaters = response.data.theatre_list; // Assuming the API response is an array of theaters
        console.log(this.theaters);
      } catch (error) {
        console.error(error);
      }
    },
    async exportTheatre(theatreId){
      // method used to export details of a particular theatre into a csv file
        try {
        const formData = {
                id: theatreId 
            };

        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        console.log(access_token)
        console.log(formData)
        //sending the post request to export api route with the id of the theatre
        const response = await axios.post('http://localhost:8081/export',formData);
        // alert(response.data.message);
        const url = window.URL.createObjectURL(new Blob([response.data]));
        // downloading the csv file generated onto the system
      
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `theatre_${theatreId}_details.csv`);
        document.body.appendChild(link);
        link.click();

        URL.revokeObjectURL(url);
        document.body.removeChild(link);
        alert('Exported')

      } catch (error) {
        console.log(error);
        alert(error);
      }
    },

    async deleteTheatre(theatreId){
        // method for deleting the theatre 
        const confirmDelete = window.confirm('Are you sure you want to delete this theatre?')
        if (!confirmDelete){
            return;
        }
      try {
        const formData = {
                id: theatreId 
            };
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;
        //sending delete request to edit theatre route of the api with the id of theatre to be deleted
        const response = await axios.delete('http://localhost:8081/edittheatre',{
          data: formData
        });
        alert(response.data.message);
        this.theaters = this.theaters.filter(theatre => theatre.id !== theatreId)
      } catch (error) {
        console.error(error);
        alert(error);
      }
    },
    summary() {
      // method which generates the summary 
      try {
        let access_token = localStorage.getItem('access_token');
        axios.defaults.headers.common['Authorization'] = 'Bearer ' + access_token;

        const response = axios.get('http://localhost:8081/summary');        

        alert('Summary Generated in the Static Folder');
      } catch (error) {
        console.error(error);
      }
    },
    updateTheatre(theatreId){
      //method which calls the update theatre router
        this.$router.push({name: 'updatetheatre', params:{id:theatreId}})
    },

    getshows(theatreId){
      // method which calls the ongoingshows router
        this.$router.push({name: 'ongoingshows', params:{id:theatreId}})
    },
    createshow(theatreId) {
        // Perform logic to add a venue here
        this.$router.push({ name: 'createshow', params: { id:theatreId } });
    },
    
    addTheatre(){
        this.$router.push('/createtheatre') //router for adding theatre
    },
    async logout(){
      //method which executes when the admin logouts 
        try{
            localStorage.removeItem('access_token') //removal of access token from the local storage
            localStorage.removeItem('username') //removal of the username from localStorage

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