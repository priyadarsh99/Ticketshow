import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'default',
      component: () => import('../views/UserLogin.vue')
    },
    {
      path: '/adminlogin',
      name: 'adminlogin',
      component:() => import('../views/AdminLogin.vue')
    },
    {
      path:'/usersignup',
      name:'usersignup',
      component:()=> import ('../views/UserSignup.vue')
    },
    {
      path:'/admin/dashboard',
      name:'admindashboard',
      component:()=> import ('../views/AdminDashboard.vue')
    },
    {
      path:'/user/dashboard',
      name:'userdashboard',
      component:()=>import ('../views/UserDashboard.vue')
    },
    {
      path:'/createtheatre',
      name: 'createtheatre',
      component:()=> import('../views/CreateTheatre.vue')

    },
    {
      path:'/updatetheatre/:id',
      name:'updatetheatre',
      component:()=> import('../views/UpdateTheatre.vue')
    },
    {
      path:'/createshow/:id',
      name: 'createshow',
      component:()=> import('../views/CreateShow.vue')
    },
    {
      path: '/ongoingshows/:id',
      name: 'ongoingshows',
      component:()=> import ('../views/ShowHomepage.vue')
    },
    {
      path: '/updateshow/:id',
      name: 'updateshow',
      component:()=> import('../views/UpdateShow.vue')
    },
    {
      path: '/bookshow/:id',
      name: 'bookshow',
      component:()=> import('../views/BookShow.vue')
    },
    {
      path: '/myprofile/:id',
      name: 'myprofile',
      component:()=> import ('../views/MyProfile.vue')
    },
    {
      path:'/rateshow/:id',
      name: 'rateshow',
      component:()=> import('../views/RateShow.vue')
    },
  ]
})

export default router
