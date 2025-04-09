<script>
import { get_interview_status, bind_cat, add_fav } from "@/API";
export default {
  data() {
    return {
        fav: this.data.is_favorite,
        isVisible: false,
        isBinded: false,
        token: '',
        imageUrl: new URL("../assets/imgs/Heart.svg", import.meta.url).href,
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
    if(this.fav){
        this.imageUrl = new URL("../assets/imgs/HeartFill.svg", import.meta.url).href
    }
    else{
        this.imageUrl = new URL("../assets/imgs/Heart.svg", import.meta.url).href
    }
    document.addEventListener('click', this.closeCat.bind(this))
    document.addEventListener("click", this.closeBind.bind(this));
  },
}
</script>

<template>

    <div class="card" @mouseenter="scaleOn" @mouseleave="scaleOff">
        <div class="card-imgBlock">
            <img class="card-imgBlock-img" @click="$emit('click', this.data.id)" :src="`http://26.48.41.80:8000/static/photos/${data.photo_url}`"  alt="" ref="cardImg">
        </div>
        <img class="card-imgBlock-like" :src="imageUrl" alt="" @click="addFav">
        <div class="card-imgBlock-name" @click="$emit('click', this.data.id)">
                <h3>{{ data.name }}</h3>
        </div>
        <div class="card-info" @click="$emit('click', this.data.id)">
            <p>{{ data.breed }} </p>
        </div>
        <div class="card-info-age" @click="$emit('click', this.data.id)">
            <p>{{ data.age }} </p>
        </div>
        <div class="card-button" @click="$emit('click', this.data.id)">
            <p> Приютить </p>
        </div>
    </div>

    <div class="black-bg" v-if="isVisible">
        <div class="open-card">
            <div class="card-imgBlock opened-card">
                <img class="card-imgBlock-img" :src="`http://26.48.41.80:8000/static/photos/${data.photo_url}`" alt="" ref="cardImg">
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
