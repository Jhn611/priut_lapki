import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Profile from './views/Profile.vue';
import Saved from './views/Saved.vue';
import Contacts from './views/Contacts.vue';
import Profile_changeinfo from './views/Profile_changeinfo.vue';
import Profile_cats from './views/Profile_cats.vue';
import Howtohelp from './views/Howtohelp.vue';
import Surrender_a_cat from './views/Surrender_a_cat.vue';
import Sobes from './views/Sobes.vue';
import LogRegIn from './views/LogRegIn.vue';
import Admin from './views/Admin.vue';

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
      path: '/profile_changeinfo',
      name: 'user_profile_changeinfo',
      component: Profile_changeinfo,
    },
    {
      path: '/profile_cats',
      name: 'user_profile_cats',
      component: Profile_cats,
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
    {
      path: '/howtohelp',
      name: 'howtohelp',
      component: Howtohelp,
    },
    {
      path: '/surrender_a_cat',
      name: 'surrender_a_cat',
      component: Surrender_a_cat,
    },
    {
      path: '/sobes',
      name: 'sobes',
      component: Sobes,
    },
    {
      path: '/auth',
      name: 'auth',
      component: LogRegIn,
    },
    {
      path: '/admin',
      name: 'admin',
      component: Admin,
    },
  ]
});

export default router;