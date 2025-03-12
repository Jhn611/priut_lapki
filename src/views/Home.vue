<script>
import CatCard from '../components/CatCard.vue';
import { get_cats } from '../API.js';
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      cats: [1, 2],
    }
  },
  props: ['command'],
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
  watch: {
    command(newCommand) {
      if (newCommand) {
        console.log('Получена команда:', newCommand);
      }
    },
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    const cats_cards = await get_cats()
    console.log(cats_cards)
    if(cats_cards){
      let x = []
      let current = []
      for(let i = 0; i < cats_cards.length; i++){
        current.push(cats_cards[i])
        if(current.length % 4 == 0){
          x.push(current)
          current = []
        }
      }
      x.push(current)
      this.cats = x
    }
    console.log(this.cats)


    const main = document.querySelector("#main")
    const height = this.cats.length * 286 + this.cats.length * 50
    main.style.height = `${height}px`
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
}
</script>

<template>
  <div class="background_card" v-for="x in cats" :key="x">
    <CatCard v-for="i in x" :key="i" :data="i"/>
  </div>
</template>

<style src="../styles/style.css"> </style>
