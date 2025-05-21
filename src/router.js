import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Announcements.vue';
import Profile from './views/Profile.vue'; // Импортируем основной компонент Profile
import Saved from './views/Saved.vue';
import Priyut from './views/Priyut.vue';
import Profile_changeinfo from './views/Profile_changeinfo.vue';
import Profile_my_ad from './views/Profile_my_ad.vue';
import Profile_my_armor from './views/Profile_my_armor.vue';
import Profile_my_priyut from './views/Profile_my_priyut.vue';
import Profile_status_sobes from './views/Profile_status_sobes.vue';
import Profile_cats from './views/Profile.vue';
import Howtohelp from './views/Howtohelp.vue';
import Post_an_ad from './views/Post_an_ad.vue';
import Sobesedovanie from './views/Sobesedovanie.vue';
import LogRegIn from './views/LogRegIn.vue';
import Admin from './views/Admin_see_ad.vue';
import Hellopage from './views/Hellopage.vue';
import Announcements from './views/Announcements.vue';
import Admin_see_ad from './views/Admin_see_ad.vue';
import Admin_list_users from './views/Admin_list_users.vue';
import Admin_list_priyuts from './views/Admin_list_priyuts.vue';
import Admin_list_priyut_for_moderation from './views/Admin_list_priyut_for_moderation.vue';
import Admin_list_ad_for_moderation from './views/Admin_list_ad_for_moderation.vue';

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
      path: '/home',
      name: 'home',
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
      path: '/admin_see_ad',
      name: 'admin_see_ad',
      component: Admin_see_ad,
    },
    {
      path: '/admin_list_priyuts',
      name: 'admin_list_priyuts',
      component: Admin_list_priyuts,
    },
    {
      path: '/admin_list_users',
      name: 'admin_list_users',
      component: Admin_list_users,
    },
    {
      path: '/admin_list_priyut_for_moderation',
      name: 'admin_list_priyut_for_moderation',
      component: Admin_list_priyut_for_moderation,
    },
    {
      path: '/admin_list_ad_for_moderation',
      name: 'admin_list_ad_for_moderation',
      component: Admin_list_ad_for_moderation,
    },
  ]
});

export default router;