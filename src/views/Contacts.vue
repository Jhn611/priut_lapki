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
        <div class="priyut_map"><div style="position:relative;overflow:hidden;"><a href="https://yandex.ru/maps/213/moscow/?utm_medium=mapframe&utm_source=maps" style="color:#eee;font-size:12px;position:absolute;top:0px;"></a><a href="https://yandex.ru/maps/213/moscow/geo/ulitsa_sofyi_kovalevskoy/10050700/?ll=37.534693%2C55.884878&utm_medium=mapframe&utm_source=maps&z=14.22" style="color:#eee;font-size:12px;position:absolute;top:14px;"></a><iframe src="https://yandex.ru/map-widget/v1/?ll=37.534693%2C55.884878&mode=search&ol=geo&ouri=ymapsbm1%3A%2F%2Fgeo%3Fdata%3DCggxMDA1MDcwMBJI0KDQvtGB0YHQuNGPLCDQnNC-0YHQutCy0LAsINGD0LvQuNGG0LAg0KHQvtGE0YzQuCDQmtC-0LLQsNC70LXQstGB0LrQvtC5IgoN9SIWQhVbi19C&z=14.22" frameborder="1" allowfullscreen="true" style="position:relative;"></iframe></div> </div>
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
