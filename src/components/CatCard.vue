<script>
import { get_interview_status, bind_cat } from "@/API";
export default {
  data() {
    return {
        fav: false,
        isVisible: false,
        isBinded: false,
    }
  },
  props: {
    data: {
      type: Object, 
      required: true, 
    },
},
  methods: {
    scaleOn(){
        const img = this.$refs.cardImg
        img.style.transform = "scale(1.1)"
    },
    scaleOff(){
        const img = this.$refs.cardImg
        img.style.transform = "scale(1.0)"
    },
    addFav(){
        this.fav = !this.fav
        const imgFav = this.$refs.cardFav
        if(this.fav){
            // хз пока чё тут
        }
    },
    openCard(){
        const body = document.body,  html = document.documentElement;
        const height = Math.max( body.scrollHeight, body.offsetHeight,
                            html.clientHeight, html.scrollHeight, html.offsetHeight );
        this.isVisible = true;
        const pad = (window.innerWidth - 1040) / 2
        const padBind = (window.innerWidth - 900) / 2
        const currentStyles = document.body.style.cssText;
        document.body.style.cssText =  currentStyles  + `--cardpad: ${pad}px; --padbind: ${padBind}px; --cardblackbgwidth: ${window.innerWidth}px; --cardblackbgheight: ${height}px`
        console.log(pad, window.innerWidth, height)
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
  async mounted() {
    document.addEventListener('click', this.closeCat.bind(this))
    document.addEventListener("click", this.closeBind.bind(this));
  },
}
</script>

<template>
    <div class="card" @mouseenter="scaleOn" @mouseleave="scaleOff" @click="openCard">
        <div class="card-imgBlock">
            <img class="card-imgBlock-img" src="../assets/imgs/cat1.jpg" alt="" ref="cardImg">
            <img class="card-imgBlock-like" src="../assets/imgs/Heart.svg" alt="" @click="addFav" ref="cardFav">
            <div class="card-imgBlock-name">
                <h3>{{ data.name }}</h3>
            </div>
        </div>
        <div class="card-info">
            <p>{{ data.breed }}</p>
        </div>
    </div>
    <div class="black-bg" v-if="isVisible">
        <div class="open-card">
            <div class="card-imgBlock opened-card">
                <img class="card-imgBlock-img" src="../assets/imgs/cat1.jpg" alt="" ref="cardImg">
                <img class="card-imgBlock-like" src="../assets/imgs/Heart.svg" alt="" @click="addFav" ref="cardFav">
            </div>
            <div class="card-infoBlock">
                <div class="card-infoBlock-name"><p>{{data.name}}</p></div>
                <div class="card-infoBlock-discription"><p>Описание</p><p class="discription">{{data.description}}</p>
                    <p class="discription">Порода: {{data.breed}}, Пол: {{data.gender}}, Возраст: {{data.age}}, Цвет: {{data.color}}.</p></div>
                <div class="card-infoBlock-btn" @click="bindCat"><p>Приютить</p></div>
            </div>
        </div>
        
        </div>
        <div class="black-bg z1002" v-if="isBinded">
            <div class="binded-cat" >
            <p>Котик забронирован за вами,<br> ждем вас в рабочее время приюта на стойке администратора в рабочее время (10:00-20:00) <br> Администратор проведет с вами личную беседу, познакомит с будущем питомцем и, в случае взаимной симпатии, оформит нужные документы.  </p>
        </div>
    </div>
        
</template>

<style src="../styles/card.css"></style>
