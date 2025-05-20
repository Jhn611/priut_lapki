import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Announcements.vue';
import Profile from './views/Profile_status_sobes.vue';
import Saved from './views/Saved.vue';
import Contacts from './views/Priyut.vue';
import Profile_changeinfo from './views/Profile_changeinfo.vue';
import Profile_cats from './views/Profile_cats.vue';
import Howtohelp from './views/Howtohelp.vue';
import Post_an_ad from './views/Post_an_ad.vue';
import Sobesedovanie from './views/Sobesedovanie.vue';
import LogRegIn from './views/LogRegIn.vue';
import Admin from './views/Admin_see_ad.vue';
import Hellopage from './views/Hellopage.vue';

const routes = [
];

const router = createRouter({
  history: createWebHistory(), // Использует HTML5 History API
  routes: [
    {
      path: '/hello_page',
      name: 'hello_page',
      props: (route) => ({ command: route.query.command }),
      component: Home,
    },
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
      path: '/sobesedovanie',
      name: 'sobesedovanie',
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