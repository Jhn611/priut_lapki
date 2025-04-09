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

      const height = this.cats.length * 650 + this.cats.length * 30;
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
            <CatCard :data="slide" @click="openCard" />
          </swiper-slide>

          <div class="swiper-button-prev"></div>
          <div class="swiper-button-next"></div>
        </swiper>
      </div>
    </div>
  </div>
  <div class="black-bg" v-if="isVisible">
    <div class="loader" v-if="load2">
      <img src="../assets/imgs/Loader.svg" alt="" />
    </div>
    <div class="open-card" v-if="!load2">
      <div class="card-open-cat">
        <img
          class="card-imgBlock-img"
          :src="`http://26.48.41.80:8000/static/photos/${cat.photo_url}`"
          alt=""
          ref="cardImg"
        />
      </div>
      <div class="oc-right">
        <p class="kotkoshka">{{ cat.gender }}</p>
        <p class="kotname">
          <b> {{ cat.name }} </b>
        </p>
        <div class="oc-zag">
          <p @click="cardPageActive = 1" style="cursor: pointer">Информация</p>
          <p @click="cardPageActive = 2" style="cursor: pointer">Описание</p>
          <p @click="cardPageActive = 3" style="cursor: pointer">История</p>
        </div>
        <div class="oc-zag-polos">
          <div class="polos1" :class="{ active: cardPageActive == 1 }"></div>
          <div class="polos2" :class="{ active: cardPageActive == 2 }"></div>
          <div class="polos3" :class="{ active: cardPageActive == 3 }"></div>
        </div>
        <div class="description_cat" v-if="cardPageActive == 2 || cardPageActive == 3">
          <p>{{ cat.description  }} </p>
        </div>
        <div class="charact_cat" v-if="cardPageActive == 1">
          <!-- <p> описание описания </p> -->
          <!-- <p> рассказ истории </p> -->
          <p>Пол: {{ cat.gender }}</p>
          <div class="pol"></div>
          <p>Возраст: {{ cat.age }}</p>
          <div class="pol-s1"></div>
          <p>Порода: {{ cat.breed }}</p>
          <div class="pol-s2"></div>
          <p>Стерилизация/кастрация: {{  cat.is_sterilized ? 'Да' : 'Нет' }}</p>
          <div class="pol-s3"></div>
          <p>Прививка от бешенства: {{ cat.has_rabies_vaccine ? 'Да' : 'Нет'}}</p>
          <div class="pol-s4"></div>
        </div>
        <div class="buttons-catcard">
          <div
            class="button-to-saved"
            style="cursor: pointer"
            v-if="!fav"
            @click="addFav(cat.id)"
          >
            <p>Добавить в избранное</p>
          </div>
          <div
            class="button-to-saved"
            style="cursor: pointer"
            v-if="fav"
            @click="addFav(cat.id)"
          >
            <p>Удалить из избранного</p>
          </div>
          <div
            class="button-to-priyutit"
            style="cursor: pointer"
            @click="bindCat(cat.id)"
          >
            <p>Приютить кота</p>
          </div>
        </div>
      </div>

      <!-- <div class="card-infoBlock">
                <div class="card-infoBlock-name"><p>{{data.name}}</p></div>
                <div class="card-infoBlock-discription"><p>Описание</p><p class="discription">{{data.description}}</p>
                    <p class="discription">Порода: {{data.breed}}, Пол: {{data.gender}}, Возраст: {{data.age}}, Цвет: {{data.color}}.</p></div>
                <div class="card-infoBlock-btn" @click="bindCat"><p>Приютить</p></div>
            </div> -->
    </div>
  </div>
  <div class="black-bg z1002" v-if="isBinded">
    <div class="binded-cat">
      <p>
        Котик забронирован за вами,<br />
        ждем вас в рабочее время приюта на стойке администратора в рабочее время
        (10:00-20:00) <br />
        Администратор проведет с вами личную беседу, познакомит с будущем
        питомцем и, в случае взаимной симпатии, оформит нужные документы.
      </p>
    </div>
  </div>
  <div class="home">
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
