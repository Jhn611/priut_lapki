import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Profile from './views/Profile.vue';
const routes = [
];

const router = createRouter({
  history: createWebHistory(), // Использует HTML5 History API
  routes: [
    {
      path: '/home',
      name: 'user_home',
      props: (route) => ({ command: route.query.command }),
      component: Home,
    },
    {
      path: '/profile',
      name: 'user_profile',
      component: Profile,
    },
  ]
});

export default router;