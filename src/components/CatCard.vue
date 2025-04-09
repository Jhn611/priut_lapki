<script>
import { get_interview_status, bind_cat, add_fav } from "@/API";
export default {
  data() {
    return {
        fav: this.data.is_favorite,
        isVisible: false,
        isBinded: false,
        token: '',
        lastClickTime: 0,
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
    getCat(){
        const now = Date.now();
        if (now - this.lastClickTime < 2000){
            this.lastClickTime = now;
            return;
        };
        this.$emit('click', this.data.id)
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
            <img class="card-imgBlock-img" @click="getCat" :src="`http://26.48.41.80:8000/static/photos/${data.photo_url}`"  alt="" ref="cardImg">
        </div>
        <img class="card-imgBlock-like" :src="imageUrl" alt="" @click="addFav">
        <div class="card-imgBlock-name" @click="getCat">
                <h3>{{ data.name }}</h3>
        </div>
        <div class="card-info" @click="getCat">
            <p>{{ data.breed }} </p>
        </div>
        <div class="card-info-age" @click="getCat">
            <p>{{ data.age }} </p>
        </div>
        <div class="card-button" @click="getCat" style="cursor: pointer">
            <p> Приютить </p>
        </div>
    </div>
        
</template>

<style src="../styles/card.css"></style>
