import { createStore } from 'vuex'

export default createStore({
    state:{
        adminToken: null 
    },
    mutations:{
        setAdminToken(state, token){
            state.adminToken = token 
        }
    },
    actions:{
        // Your other actions
    },
    getters:{
        // Your other getters
    }
})