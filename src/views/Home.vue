<script>
import CatCard from "../components/CatCard.vue";
import { get_cats, search_cats, get_cat } from "../API.js";
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
      token: '',
      cat: [],
      fav: false,
      isVisible: false,
      load2: false,
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
    async addFav(){
        this.fav = !this.fav
        if(this.fav){
            this.imageUrl = new URL("../assets/imgs/HeartFill.svg", import.meta.url).href
        }
        else{
            this.imageUrl = new URL("../assets/imgs/Heart.svg", import.meta.url).href
        }
        try{
            this.token = localStorage.getItem('token')
            if(this.token && this.token != ''){
                const json = await get_interview_status(this.token);
                if(json == 401){
                    localStorage.setItem("token", '') 
                }else{
                    await add_fav(this.data.id, this.token)
                }
            }
        }catch{

        }
    },
    async openCard(id){
        const body = document.body,  html = document.documentElement;
        const height = Math.max( body.scrollHeight, body.offsetHeight,
                            html.clientHeight, html.scrollHeight, html.offsetHeight );
        
        const pad = (window.innerWidth - 1040) / 2
        const padBind = (window.innerWidth - 900) / 2
        const currentStyles = document.body.style.cssText;
        document.body.style.cssText =  currentStyles  + `--cardpad: ${pad}px; --padbind: ${padBind}px; --cardblackbgwidth: ${window.innerWidth}px; --cardblackbgheight: ${height}px`
        console.log(pad, window.innerWidth, height)

        this.load2 = true;
        try{
          this.cat = await get_cat(id, this.token);
          console.log(this.cat)
          this.isVisible = true;
          this.load2 = false;
        }catch{
          console.log("PIZDARIKI")
          this.load2 = false;
          this.isVisible = false;
        }
    },
    closeCat(e) {
      if (!this.$el.contains(e.target) && !e.target.closest('.open-card') && !e.target.closest('.card')) { 
        this.isVisible = false;
      }
    },
    async bindCat(){
        this.token = localStorage.getItem("token");
        if (this.token && this.token != "") {
            const json = await get_interview_status(this.token);
        if(json == 401){
            localStorage.setItem("token", '') 
        }else{
            this.status = json['status'];
            if(this.status == 'passed'){
                const json = await bind_cat(this.data.id, this.token);
                this.isBinded = true
            }
        }
        }
    },
    closeBind(e) {
      if (
        !this.$el.contains(e.target) &&
        !e.target.closest(".binded-cat") &&
        !e.target.closest(".card-infoBlock-btn")
        &&
        !e.target.closest(".card") &&
        !e.target.closest(".open-card") 
      ) {
        this.isVisible = false;
        this.isBinded = false;
        
      }
    },
  },
  watch: {
    async command(newCommand) {
      if (newCommand) {
        this.load = true;
        try {
          this.token = localStorage.getItem("token")
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
      this.token = localStorage.getItem("token")
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

    if(this.fav){
        this.imageUrl = new URL("../assets/imgs/HeartFill.svg", import.meta.url).href
    }
    else{
        this.imageUrl = new URL("../assets/imgs/Heart.svg", import.meta.url).href
    }
    document.addEventListener('click', this.closeCat.bind(this))
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
        <div class="open-card">
            <div class="card-imgBlock opened-card">
                <img class="card-imgBlock-img" :src="`http://26.48.41.80:8000/static/photos/${cat.photo_url}`" alt="" ref="cardImg">
                <img class="card-imgBlock-like" src="../assets/imgs/Heart.svg" alt="" @click="addFav" ref="cardFav">
            </div>
            <div class="card-infoBlock">
                <div class="card-infoBlock-name"><p>{{cat.name}}</p></div>
                <div class="card-infoBlock-discription"><p>Описание</p><p class="discription">{{cat.description}}</p>
                    <p class="discription">Порода: {{cat.breed}}, Пол: {{cat.gender}}, Возраст: {{cat.age}}, Цвет: {{cat.color}}.</p></div>
                <div class="card-infoBlock-btn" @click="bindCat"><p>Приютить</p></div>
            </div>
        </div>
        
        </div>
        <div class="black-bg z1002" v-if="isBinded">
            <div class="binded-cat" >
            <p>Котик забронирован за вами,<br> ждем вас в рабочее время приюта на стойке администратора в рабочее время (10:00-20:00) <br> Администратор проведет с вами личную беседу, познакомит с будущем питомцем и, в случае взаимной симпатии, оформит нужные документы.  </p>
        </div>
    </div>
  <div class="loader" v-if="load">
    <img src="../assets/imgs/Loader.svg" alt="" />
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