import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import ChatDetailView from '@/views/ChatDetailView.vue'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/chats',
    name: 'chats',
    component: () => import(/* webpackChunkName: "about" */ '../views/ChatsView.vue'),
    children: [
      {
        path: ":id",
        name: "chat-detail",
        component: ChatDetailView
      }
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      hideNavbar: true,
     }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
]

const router = createRouter({
  // mode: 'history',
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(function(to, from, next){
    var isAuthenticated = false;
    //this is just an example. You will have to find a better or 
    // centralised way to handle you localstorage data handling 
    if(localStorage.getItem('access_token'))
      isAuthenticated = true;
    else
      isAuthenticated= false;
    if ( to.name !== 'login' && !isAuthenticated ){
      next({
        name: 'login',
        replace: true
      })
    } else {
      next();
    }
})

export default router
