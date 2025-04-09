<script>
import { get_favorite } from "../API.js";
import CatCard from "../components/CatCard.vue";
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation, Pagination, A11y } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      load: false,
      cats: [],
      token: "",
      modules: [Navigation, Pagination, A11y],
      swiperOptions: {
        slidesPerView: 3,
        centeredSlides: true,
        spaceBetween: 30,
        loop: true,
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
        breakpoints: {
          640: {
            slidesPerView: 1.3,
            centeredSlides: true
          },
          768: {
            slidesPerView: 2,
            centeredSlides: true
          },
          1024: {
            slidesPerView: 3,
            centeredSlides: true
          }
        },
      }
    };
  },
  components: {
    //тут импортируются компоненты (например карточка)
    CatCard,
    Swiper,
    SwiperSlide,
  },
  computed: {
    // тут функции которые что-то считают и возвращают что-то (пока можно не использовать, это для оптимизации)
  },
  methods: {
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
    onSwiper(swiper) {
      console.log(swiper);
    },
    onSlideChange() {
      console.log("slide change");
    },
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.load = true;
      try {
        const cats_cards = await get_favorite(this.token);
        console.log("карточки: ", cats_cards);
        if (cats_cards) {
          let x = [];
          let current = [];
          for (let i = 0; i < cats_cards.length; i++) {
            current.push(cats_cards[i]);
            if (current.length % 4 == 0) {
              x.push(current);
              current = [];
            }
          }
          if (current.length != 0) {
            x.push(current);
          }
          this.cats = x;
        }
        console.log(this.cats);

        const height = this.cats.length * 650 + this.cats.length * 30;
        const currentStyles = document.body.style.cssText;
        document.body.style.cssText =
          currentStyles + `--mainHeight: ${height}px`;
        this.load = false;
      } catch {
        this.load = false;
      }
    }
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="saved_all">
    <div class="saved_cats"><a> Котики, которые вам понравились </a></div>
    <div class="background_card_container" v-if="!load && cats">
      <div class="background_card" v-for="x in cats" :key="x">
        <div class="slider-wrapper">
        <swiper
          v-bind="swiperOptions"
          :modules="modules"
          class="my-swiper"
          @swiper="onSwiper"
          @slideChange="onSlideChange"
        >
          <swiper-slide v-for="(slide, slideIndex) in x" :key="slideIndex">
            <CatCard :data="slide" />
          </swiper-slide>
          
          <div class="swiper-button-prev"></div>
          <div class="swiper-button-next"></div>
        </swiper>
      </div>
      </div>
    </div>
    <div class="saved_cats_if" v-if="cats.length == 0 && !load">
      <a class="sce_text">
        Здесь пока ничего нет, надеемся вы найдете любимчиков!
      </a>
    </div>
    <div class="loader" v-if="load">
      <img src="../assets/imgs/Loader.svg" alt="" />
    </div>
    <div class="saved_cats_else" v-if="!load">
      <a class="sce_text">
        Добавляйте котиков не только в избранное, но и в свой дом!
      </a>
    </div>
  </div>

  
</template>

<style scoped>
.slider-wrapper {
  position: relative;
  width: 950px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.my-swiper {
  width: 100%;
  height: auto;
  padding: 20px;
}

.swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
  transition: transform 0.3s ease;
}

.swiper-slide-active {
  transform: scale(1.05);
  z-index: 1;
}

/* Стили для кнопок навигации */
.swiper-button-prev,
.swiper-button-next {
  color: white;
  background: #41220b7d;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.swiper-button-prev::after,
.swiper-button-next::after {
  font-size: 20px;
}

.swiper-button-prev {
  left: 0;
}

.swiper-button-next {
  right: 0;
}

.background_card_container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}
</style>
