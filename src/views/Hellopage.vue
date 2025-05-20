<script>
import CatCard from "../components/CatCard.vue";
import {
  get_cats,
  search_cats,
  get_cat,
  get_interview_status,
  add_fav,
  bind_cat,
} from "../API.js";
import { Swiper, SwiperSlide } from "swiper/vue";
import { Navigation, Pagination, A11y } from "swiper/modules";
import "swiper/css";
import "swiper/css/navigation";
import "swiper/css/pagination";

export default {
  data() {
    return {
      cats: [1, 2],
      load: false,
      token: "",
      cat: [],
      fav: false,
      isVisible: false,
      load2: false,
      binded: false,
      isBinded: false,
      lastClickTime: 0,
      changed: false,
      cardPageActive: 1,
      modules: [Navigation, Pagination, A11y],
      swiperOptions: {
        slidesPerView: 3,
        centeredSlides: true,
        spaceBetween: 30,
        loop: true,
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
        breakpoints: {
          640: {
            slidesPerView: 1.3,
            centeredSlides: true,
          },
          768: {
            slidesPerView: 2,
            centeredSlides: true,
          },
          1024: {
            slidesPerView: 3,
            centeredSlides: true,
          },
        },
      },
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
    async addFav(id) {
      this.fav = !this.fav;
      try {
        this.token = localStorage.getItem("token");
        if (this.token && this.token != "") {
          const json = await get_interview_status(this.token);
          if (json == 401) {
            localStorage.setItem("token", "");
            this.fav = !this.fav;
          } else {
            console.log("Я ТУТА");
            if (typeof id == "number") {
              this.changed = true;
              await add_fav(id, this.token);
            }
          }
        }
      } catch {}
    },
    async openCard(id) {
      const body = document.body,
        html = document.documentElement;
      const height = Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.clientHeight,
        html.scrollHeight,
        html.offsetHeight
      );

      const pad = (window.innerWidth - 1040) / 2;
      const padBind = (window.innerWidth - 900) / 2;
      const currentStyles = document.body.style.cssText;
      document.body.style.cssText =
        currentStyles +
        `--cardpad: ${pad}px; --padbind: ${padBind}px; --cardblackbgwidth: ${window.innerWidth}px; --cardblackbgheight: ${height}px`;
      console.log(pad, window.innerWidth, height);
      if (typeof id == "number") {
        this.load2 = true;
        try {
          this.cat = [];
          this.cat = await get_cat(id, this.token);

          console.log(this.cat);
          this.fav = this.cat.is_favorite;
          this.isVisible = true;
          this.load2 = false;
        } catch {
          this.load2 = false;
          this.isVisible = false;
        }
      }
    },
    closeCat(e) {
      if (
        !this.$el.contains(e.target) &&
        !e.target.closest(".open-card") &&
        !e.target.closest(".card") &&
        !e.target.closest(".button-to-saved")
      ) {
        this.isVisible = false;
        if (this.changed) {
          window.location.reload();
        }
      }
    },
    async bindCat(id) {
      this.token = localStorage.getItem("token");
      if (this.token && this.token != "") {
        const json = await get_interview_status(this.token);
        if (json == 401) {
          localStorage.setItem("token", "");
        } else {
          this.status = json["status"];
          if (this.status == "passed") {
            if (typeof id == "number") {
              this.changed = true;
              const json = await bind_cat(id, this.token);
            }
            this.isBinded = true;
          }
        }
      }
    },
    closeBind(e) {
      if (
        !this.$el.contains(e.target) &&
        !e.target.closest(".binded-cat") &&
        !e.target.closest(".card-infoBlock-btn") &&
        !e.target.closest(".card") &&
        !e.target.closest(".open-card") &&
        !e.target.closest(".button-to-saved")
      ) {
        this.isVisible = false;
        this.isBinded = false;
        if (this.changed) {
          window.location.reload();
        }
      }
    },
    scrollTo(id) {
      const element = document.querySelector(id);
      
      const offset = 140;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    },
  },
  watch: {
    async command(newCommand) {
      if (newCommand) {
        this.load = true;
        try {
          this.token = localStorage.getItem("token");
          console.log("Получена команда:", newCommand);
          const cats_cards = await search_cats(newCommand, this.token);
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
          const height = this.cats.length * 620 + this.cats.length * 30;
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
      this.token = localStorage.getItem("token");
      const cats_cards = await get_cats(0, 12, this.token);
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

      const height = this.cats.length * 620 + this.cats.length * 30;
      const currentStyles = document.body.style.cssText;
      document.body.style.cssText = currentStyles + `--mainHeight: ${height}px`;
      this.load = false;
    } catch {
      this.load = false;
    }

    document.addEventListener("click", this.closeCat.bind(this));
    document.addEventListener("click", this.closeBind.bind(this));
  },
};
</script>

<template>

привет страница

  <div class="home" v-if="load">
    <div class="loader" v-if="load">
      <img src="../assets/imgs/Loader.svg" alt="" />
    </div>
  </div>
</template>

<style scoped>
.slider-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 950px;
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
