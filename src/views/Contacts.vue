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
  <div class="contacts_all"> 
    <div class="bgr_photo_map"> 
        <div class="image_priyut"> 
            <div class="metro_adres">
                <div class="bgr_metro"> <p> м. Селигерская </p></div>
                <div class="bgr_adres"> <p> ул. Софьи Ковалевской 228 </p></div>
            </div>
        </div>
        <div class="priyut_map"> </div>
    </div>
    <div class="bgr_info_video"> 
        <div class="div_ph"> <p> Номер телефона </p></div>
        <p> +7 (999) 888 33 55 </p>
        <div class="div_adres"> <p> Адрес </p></div>
        <p> г. Москва ул. Софьи Ковалевской 228</p>
        <div class="div_howdobr"> <p> Как добраться? </p></div>
        <p> Видео как добраться от метро </p>
        <div class="video"> </div>

    </div>
  </div>  

</template>

<style src="../styles/style.css"></style>
