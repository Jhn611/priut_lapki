import { createRouter, createWebHistory } from 'vue-router';
import Saved from './views/Saved.vue';
import Priyut from './views/Priyut.vue';
import Profile_changeinfo from './views/Profile_changeinfo.vue';
import Profile_cats from './views/Profile_cats.vue';
import Howtohelp from './views/Howtohelp.vue';
import Post_an_ad from './views/Post_an_ad.vue';
import Sobesedovanie from './views/Sobesedovanie.vue';
import LogRegIn from './views/LogRegIn.vue';
import Admin from './views/Admin_see_ad.vue';
import Hellopage from './views/Hellopage.vue';
import Announcements from './views/Announcements.vue';

const routes = [
];

const router = createRouter({
  history: createWebHistory(), // Использует HTML5 History API
  routes: [
    {
      path: '/hellopage',
      name: 'hellopage',
      // props: (route) => ({ command: route.query.command }),
      component: Hellopage,
    },
    {
      path: '/announcements',
      name: 'announcements',
      // props: (route) => ({ command: route.query.command }),
      component: Announcements,
    },
    {
      path: '/priyut',
      name: 'priyut',
      component: Priyut,
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
      path: '/howtohelp',
      name: 'howtohelp',
      component: Howtohelp,
    },
    {
      path: '/post_an_ad',
      name: 'post_an_a',
      component: Post_an_ad,
    },
    {
      path: '/sobesedovanie',
      name: 'sobesedovanie',
      component: Sobesedovanie,
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