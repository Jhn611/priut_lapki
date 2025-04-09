<script>
import CatCard from "../components/CatCard.vue";
import { get_cats, search_cats } from "../API.js";
import { Swiper, SwiperSlide } from 'swiper/vue';
import { Navigation, Pagination, A11y } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

export default {
  data() {
    return {
      cats: [1, 2],
      load: false,
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
        }
      }
    };
  },
  props: ["command"],
  components: {
    CatCard,
    Swiper,
    SwiperSlide,
  },
  methods: {
    onSwiper(swiper) {
      console.log(swiper);
    },
    onSlideChange() {
      console.log("slide change");
    },
  },
  watch: {
    async command(newCommand) {
      if (newCommand) {
        this.load = true;
        try {
          console.log("Получена команда:", newCommand);
          const cats_cards = await search_cats(newCommand);
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
          const height = this.cats.length * 286 + this.cats.length * 30;
          const currentStyles = document.body.style.cssText;
          document.body.style.cssText =
            currentStyles + `--mainHeight: ${height}px`;
          this.load = false;
        } catch {
          this.load = false;
        }
      }
    },
  },

  async mounted() {
    this.load = true;
    try {
      const cats_cards = await get_cats();
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

      const height = this.cats.length * 286 + this.cats.length * 30;
      const currentStyles = document.body.style.cssText;
      document.body.style.cssText = currentStyles + `--mainHeight: ${height}px`;
      this.load = false;
    } catch {
      this.load = false;
    }
  },
};
</script>

<template>
  <div class="background_card_container" v-if="!load">
    <div class="background_card" v-for="(x, index) in cats" :key="index">
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
  <div class="loader" v-if="load">
    <img src="../assets/imgs/Loader.svg" alt="" />
  </div>
</template>

<style scoped>
.slider-wrapper {
  position: relative;
  width: 950px;
  margin: 0 auto;
  padding: 20px 0;
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
  background: rgba(0, 0, 0, 0.5);
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