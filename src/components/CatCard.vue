<script>
export default {
  data() {
    return {
        fav: false,
    }
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
  },
}
</script>

<template>
    <div class="card" @mouseenter="scaleOn" @mouseleave="scaleOff">
        <div class="card-imgBlock">
            <img class="card-imgBlock-img" src="../assets/imgs/cat1.jpg" alt="" ref="cardImg">
            <img class="card-imgBlock-like" src="../assets/imgs/Heart.svg" alt="" @click="addFav" ref="cardFav">
            <div class="card-imgBlock-name">
                <h3>КотоБубсик</h3>
            </div>
        </div>
        <div class="card-info">
            <p>Он милашка</p>
        </div>
    </div>
</template>

<style src="../styles/card.css"></style>
