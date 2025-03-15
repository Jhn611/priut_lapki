<script>
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
    };
  },
  components: {
    //тут импортируются компоненты (например карточка)
    CatCard,
  },
  computed: {
    // тут функции которые что-то считают и возвращают что-то (пока можно не использовать, это для оптимизации)
  },
  methods: {
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="background_pr_iz"> 
  <div class="background_profile">
    <div class="profile_setup">
      <div class="bgr_avatarka">
        <div class="p_NS"><p>ИТ</p></div>
      </div>
      <div class="Name_Subname">
        <p class="Name">Иван</p>
        <p class="Subname">Тимофеев</p>
      </div>
    </div>

    <div class="meaning">
      <img src="../assets/imgs/Rectangle.svg" />
      <p class="text_mean"> Любитель котиков, который может подарить счастливую жизнь и любимый дом
        коту. </p>
        <p class="text_mean_gpt">(Сгенерированно Yandex GPT)</p>
    </div>

    <div class="bgr_change_pr"><a> Изменить профиль </a></div>
    <div class="bgr_sobes"><a> Пройти собеседование </a></div>
  </div>

  <div class="background_izbr_pr"> </div>
  </div>
</template>

<style src="../styles/style.css"></style>
