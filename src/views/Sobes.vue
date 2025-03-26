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
  <div class="sobesedovanie_all"> 
    <div class="bgr_sobesedovanie"> 
        <div class="sobesedovanie_text"> <a> Cобеседование </a></div>
        <div class="sobesedovanie_predict"> <p> Перед тем, как приютить кошку, вам нужно пройти собеседование. <br> Пожалуйста, заполните анкету: </p> </div>
        <div class="sobesedovanie_anketa_all"> 
        <p> Почему вы решили завести кошку? </p>
        <textarea class="custom-input3"> </textarea>
        <p> Были ли у вас животные раньше? Если да, что с ними стало? </p>
        <textarea class="custom-input3"> </textarea>
        <p> Почему вы выбрали именно этого кота/кошку? </p>
        <textarea class="custom-input3"> </textarea>
        <p> Где вы живете? </p>
        <select id="housing" v-model="selectedHousing" class="custom-select">
            <option value="house">Частный дом</option>
            <option value="apartment">Квартира</option>
            <option value="rented-apartment">Съемная квартира</option>
        </select>
        <p> Каким кормом вы планируете кормить питомца? </p>
        <select id="feeding" v-model="selectedHousing" class="custom-select">
            <option value="cheep"> Бюджетный корм (Whiskas, Feliks, Kitekat и т.д.)</option>
            <option value="premium"> Корм премиум класса (Farmina, Royal Canin, Purina и т.д.)</option>
            <option value="super premium">Корм супер премиум класса(Schesir, Nero Gold, Monge и т.д.)</option>
        </select>
        <p> Опишите вашу реакцию, когда кошка испортит обои или мебель: </p>
        <textarea class="custom-input3"> </textarea>
        <p> Как будете справляться с кошачьей шерстью и когтеточением? </p>
        <textarea class="custom-input3"> </textarea>
        <p>Готовы ли вы к возможным болезням кошки, лечению и уходу за ней в старости?</p>
    <div class="radio-group">
      <label class="custom-radio">
        <input type="radio" name="health-care" value="yes" v-model="healthCare" />
        <span class="radio-mark"></span>
        <span class="radio-label">Готов(а)</span>
      </label>

      <label class="custom-radio">
        <input type="radio" name="health-care" value="no" v-model="healthCare" />
        <span class="radio-mark"></span>
        <span class="radio-label">Не уверен</span>
      </label>
    </div>

    <p>Осознаёте ли, что если животное окажется в плохих условиях, приют оставляет за собой право его изъять?</p>
    <div class="radio-group">
      <label class="custom-radio">
        <input type="radio" name="shelter-rights" value="yes" v-model="shelterRights" />
        <span class="radio-mark"></span>
        <span class="radio-label">Да</span>
      </label>

      <label class="custom-radio">
        <input type="radio" name="shelter-rights" value="no" v-model="shelterRights" />
        <span class="radio-mark"></span>
        <span class="radio-label">Нет, приют не имеет на это право</span>
      </label>
    </div>

    <p>Вы готовы заключить договор с приютом об ответственном содержании животного?</p>
    <div class="radio-group">
      <label class="custom-radio">
        <input type="radio" name="contract" value="yes" v-model="contractAgreement" />
        <span class="radio-mark"></span>
        <span class="radio-label">Да</span>
      </label>

      <label class="custom-radio">
        <input type="radio" name="contract" value="no" v-model="contractAgreement" />
        <span class="radio-mark"></span>
        <span class="radio-label">Нет</span>
      </label>
    </div>
    </div>
    </div>
  </div>
</template>

<style src="../styles/style.css"></style>
