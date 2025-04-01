<script>
import { post_interview } from "../API.js";
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      why:null,
      animalBefore:null,
      choose:null,
      selectedHousing:null,
      selectedFood:null,
      reaction:null,
      wool:null,
      healthCare:null,
      shelterRights:null,
      contractAgreement:null,
      token: null,
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
    async send(){
      const interview = await post_interview(this.why, this.animalBefore, this.choose,this.selectedHousing,this.selectedFood,this.reaction,this.wool, this.healthCare,this.shelterRights,this.contractAgreement, this.token);
      this.$router.push("/profile");
    },
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    this.token = localStorage.getItem('token');
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="sobesedovanie_all">
    <div class="bgr_sobesedovanie">
      <div class="sobesedovanie_text"><a> Cобеседование </a></div>
      <div class="sobesedovanie_predict">
        <p>
          Перед тем, как приютить кошку, вам нужно пройти собеседование. <br />
          Пожалуйста, заполните анкету:
        </p>
      </div>
      <div class="sobesedovanie_anketa_all">
        <p>Почему вы решили завести кошку?</p>
        <textarea v-model="why" class="custom-input3"> </textarea>
        <p>Были ли у вас животные раньше? Если да, что с ними стало?</p>
        <textarea v-model="animalBefore" class="custom-input3"> </textarea>
        <p>Почему вы выбрали именно этого кота/кошку?</p>
        <textarea v-model="choose" class="custom-input3"> </textarea>
        <p>Где вы живете?</p>
        <select id="housing" v-model="selectedHousing" class="custom-select">
          <option value="Частный дом">Частный дом</option>
          <option value="Квартира">Квартира</option>
          <option value="Съемная квартира">Съемная квартира</option>
        </select>
        <p>Каким кормом вы планируете кормить питомца?</p>
        <select id="feeding" v-model="selectedFood" class="custom-select">
          <option value="Бюджетный корм (Whiskas, Feliks, Kitekat и т.д.)">
            Бюджетный корм (Whiskas, Feliks, Kitekat и т.д.)
          </option>
          <option value="Корм премиум класса (Farmina, Royal Canin, Purina и т.д.)">
            Корм премиум класса (Farmina, Royal Canin, Purina и т.д.)
          </option>
          <option value="Корм супер премиум класса(Schesir, Nero Gold, Monge и т.д.)">
            Корм супер премиум класса(Schesir, Nero Gold, Monge и т.д.)
          </option>
        </select>
        <p>Опишите вашу реакцию, когда кошка испортит обои или мебель:</p>
        <textarea v-model="reaction" class="custom-input3"> </textarea>
        <p>Как будете справляться с кошачьей шерстью и когтеточением?</p>
        <textarea v-model="wool" class="custom-input3"> </textarea>
        <p>
          Готовы ли вы к возможным болезням кошки, лечению и уходу за ней в
          старости?
        </p>
        <div class="radio-group">
          <label class="custom-radio">
            <input
              type="radio"
              name="health-care"
              value="Готов(а)"
              v-model="healthCare"
            />
            <span class="radio-mark"></span>
            <span class="radio-label">Готов(а)</span>
          </label>

          <label class="custom-radio">
            <input
              type="radio"
              name="health-care"
              value="Не уверен"
              v-model="healthCare"
            />
            <span class="radio-mark"></span>
            <span class="radio-label">Не уверен</span>
          </label>
        </div>

        <p>
          Осознаёте ли, что если животное окажется в плохих условиях, приют
          оставляет за собой право его изъять?
        </p>
        <div class="radio-group">
          <label class="custom-radio">
            <input
              type="radio"
              name="shelter-rights"
              value="Да"
              v-model="shelterRights"
            />
            <span class="radio-mark"></span>
            <span class="radio-label">Да</span>
          </label>

          <label class="custom-radio">
            <input
              type="radio"
              name="shelter-rights"
              value="Нет, приют не имеет на это право"
              v-model="shelterRights"
            />
            <span class="radio-mark"></span>
            <span class="radio-label">Нет, приют не имеет на это право</span>
          </label>
        </div>

        <p>
          Вы готовы заключить договор с приютом об ответственном содержании
          животного?
        </p>
        <div class="radio-group">
          <label class="custom-radio">
            <input
              type="radio"
              name="contract"
              value="Да"
              v-model="contractAgreement"
            />
            <span class="radio-mark"></span>
            <span class="radio-label">Да</span>
          </label>

          <label class="custom-radio">
            <input
              type="radio"
              name="contract"
              value="Нет"
              v-model="contractAgreement"
            />
            <span class="radio-mark"></span>
            <span class="radio-label">Нет</span>
          </label>
        </div>
        <div @click="send" class="btn">
          <p>Отправить</p>
        </div>
        <div class="empty"></div>
      </div>
    </div>
  </div>
</template>

<style src="../styles/style.css"></style>
