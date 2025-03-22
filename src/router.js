import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Profile from './views/Profile.vue';
import Saved from './views/Saved.vue';
import Contacts from './views/Contacts.vue';

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
    {
      path: '/saved',
      name: 'user_saved',
      component: Saved,
    },
    {
      path: '/contacts',
      name: 'contacts',
      component: Contacts,
    },
  ]
});

export default router;