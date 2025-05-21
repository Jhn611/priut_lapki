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
    //header
    changePageToPriyut() {
      this.$router.push("/hellopage");
    },
    changePageToPriyut() {
      this.$router.push("/saved");
    },
    changePageToProfile() {
      this.$router.push("/profile_changeinfo");
    },
    changePageToPriyut() {
      this.$router.push("/announcements");
    },
    changePageToSaved() {
      this.$router.push("/post_an_ad");
    },
    changePageToHowtohelp() {
      this.$router.push("/sobesevodanie");
    },
    //other
    changePageToHome() {
      this.$router.push("/priyut");
    },
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
  <div class="priyut_all">
    <div class="bgr_photo_map">
      <div class="image_priyut">
      </div>
      <div class="priyut_map">
        <div style="position: relative; overflow: hidden">
          <a
            href="https://yandex.ru/maps/213/moscow/?utm_medium=mapframe&utm_source=maps"
            style="color: #eee; font-size: 12px; position: absolute; top: 0px"
          ></a
          ><a
            href="https://yandex.ru/maps/213/moscow/geo/ulitsa_sofyi_kovalevskoy/10050700/?ll=37.534693%2C55.884878&utm_medium=mapframe&utm_source=maps&z=14.22"
            style="color: #eee; font-size: 12px; position: absolute; top: 14px"
          ></a
          ><iframe
            src="https://yandex.ru/map-widget/v1/?ll=37.534693%2C55.884878&mode=search&ol=geo&ouri=ymapsbm1%3A%2F%2Fgeo%3Fdata%3DCggxMDA1MDcwMBJI0KDQvtGB0YHQuNGPLCDQnNC-0YHQutCy0LAsINGD0LvQuNGG0LAg0KHQvtGE0YzQuCDQmtC-0LLQsNC70LXQstGB0LrQvtC5IgoN9SIWQhVbi19C&z=14.22"
            frameborder="1"
            allowfullscreen="true"
            style="position: relative"
          ></iframe>
        </div>
      </div>
    </div>
    <div class="bgr_info_video">
      <div class="p1_priyut">
        <p class="p1_1_priyut"> Приют </p>
        <p class="p1_2_priyut"> "Любимчики"</p>
      </div>
      <div class="p2_priyut">
        Адрес
      <div class="priyut_div1"> </div>
      </div>
      <div class="p3_priyut">
        Номер телефона
      <div class="priyut_div2"> </div>
      </div>
      <div class="p4_priyut">
        Описание
      <div class="priyut_div3"> </div>
      </div>
      <div class="button_to_ad_priyut"> Просмотреть <br> объявления от приюта </div>
    </div>
  </div>  
</template>

<style src="../styles/style.css"></style>
