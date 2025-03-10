import { createRouter, createWebHistory } from 'vue-router';

const routes = [
];

const router = createRouter({
  history: createWebHistory(), // Использует HTML5 History API
  routes // Передайте массив маршрутов
});

export default router;