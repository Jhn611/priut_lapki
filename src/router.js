import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Announcements.vue';
import Profile from './views/Profile.vue'; // Импортируем основной компонент Profile
import Saved from './views/Saved.vue';
import Contacts from './views/Priyut.vue';
import Profile_changeinfo from './views/Profile_changeinfo.vue';
import Profile_my_ad from './views/Profile_my_ad.vue';
import Profile_my_armor from './views/Profile_my_armor.vue';
import Profile_my_priyut from './views/Profile_my_priyut.vue';
import Profile_status_sobes from './views/Profile_status_sobes.vue';
import Profile_cats from './views/Profile.vue';
import Howtohelp from './views/Howtohelp.vue';
import Surrender_a_cat from './views/Post_an_ad.vue';
import Sobes from './views/Sobesedovanie.vue';
import LogRegIn from './views/LogRegIn.vue';
import Admin from './views/Admin_see_ad.vue';

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
      component: Profile, // Используем основной Profile.vue как родительский компонент
      children: [
        {
          path: '',
          redirect: '/profile/status' // Перенаправляем на статус по умолчанию
        },
        {
          path: 'edit',
          component: Profile_changeinfo
        },
        {
          path: 'status', 
          component: Profile_status_sobes
        },
        {
          path: 'armor', 
          component: Profile_my_armor
        },
        {
          path: 'ad', 
          component: Profile_my_ad
        },
        {
          path: 'priyut', 
          component: Profile_my_priyut
        },
      ]
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