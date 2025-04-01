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
    changePageToSurrenderaCat(){
      this.$router.push('/surrender_a_cat');
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
  <div class="background_surrender"> 
  <div class="background_surrender_left">
    <div class="anketa1_all"> 
        <div class="surrender_zag"> <p> Сдать кошку в приют </p> </div>
        <p> Если по каким-то жизненым обстоятельствам вам необходимо пристроить кошку, вы можете сдать ее к нам в приют. Для этого заполните анкету: </p>
        <p> Имя питомца </p>
        <div class="photo_cat_bgr"> <p> Фото питомца </p> </div>
    </div>
    <div class="btn">
          <p>Отправить</p>
    </div>
  </div>

  <div class="background_surrender_right"> 
    <div class="anketa2_all"> 
        <p>Расскажите, почему отдаете кошку</p>
        <label class="input">
            <input
              
              class="input__field color2"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Например, переезд или нашли на улице</span>
        </label>

        <p>Расскажите, какими болезнями болела/болеет кошка</p>
        <label class="input">
            <input
              
              class="input__field color2"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Важны все болезни</span>
        </label>

        <p>Питомец стерилизован/кастрирован?</p>
        <label>
            <input type="radio" name="sterilized" class="custom-radio" checked> <p> Да </p>
        </label>
        <label>
            <input type="radio" name="sterilized" class="custom-radio"> <p> Нет </p>
        </label>

        <p>Делалась ли прививка от бешенства, если да, то когда?</p>
        <label class="input">
            <input
              
              class="input__field color2"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Например, сентябрь 2023 года</span>
        </label>

        <p>Ваш номер телефона для связи</p>
        <label class="input">
            <input
              
              class="input__field color2"
              type="text"
              placeholder=" "
            />
            <span class="input__label">Например: +79321112723</span>
        </label>
    </div>
    <!-- <div class="bgr_status_sobes"> 
    </div> -->
  </div>
  </div>
</template>

<style src="../styles/style.css"></style>
