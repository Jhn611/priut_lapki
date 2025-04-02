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
    changePageToProfile(){
      this.$router.push('/profile');
    },
    changePageToHome(){
      this.$router.push('/home');
    },
    changePageToSaved(){
      this.$router.push('/saved');
    },
    changePageToContacts(){
      this.$router.push('/contacts');
    },
    changePageToHowtohelp(){
      this.$router.push('/howtohelp');
    },
    changePageAdmin(){
      this.$router.push('/admin');
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
  <div class="adminbroni_all"> 
    <div class="bgr_adminbroni_cats"> 
        <p class="text_broni"> <b> Список броней </b></p>
        <div class="search-bar">
            <input type="text" v-model="query" placeholder="Поиск..." />
            <button @click="search">
            <img src="../assets/imgs/Search.svg"  />
            </button>
        </div>
        <div class="bgr_bronicats">
                <div class="photo_cat"> </div>

                <div class="data_broni">
                    <div class="all_bgr_imya">
                        <div class="bgr_imya"> 
                            <p class="p_imya"> Имя кошки </p>
                            <div class="bgr_imya_cat"> <p class="p_imya_cat"> Джесси </p></div>
                        </div>
                    </div>

                    <div class="bgr_imya"> 
                            <p class="p_imya"> Имя клиента </p>
                            <div class="bgr_imya_cat"> <p class="p_imya_cat"> Джесси </p></div>
                    </div>
                    <div class="bgr_imya"> 
                            <p class="p_imya"> Номер телефона </p>
                            <div class="bgr_imya_cat"> <p class="p_imya_cat"> Джесси </p></div>
                    </div>
                </div>
                <div class="button_krest"> <img src="../assets/imgs/krest.svg"  /> </div>
        </div>
    </div>
  </div>
</template>

<style src="../styles/style.css"></style>
