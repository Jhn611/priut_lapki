<script>
export default {
  data() {
    return {
        searchString:"",
    }
  },
  props: {
    modelValue: {
      type: String,
      required: true,
    },
  },
  methods: {
    updateValue() {
      this.$emit('update:modelValue', this.searchString); 
    },
  },
}
</script>

<template>
    <div class="search">
        <div class="search-input_block">
            <input type="text" placeholder="Поиск с GigaChat" v-model="searchString">
        </div>
        <div class="search-button_block">
            <img src="../assets/imgs/Search.svg" alt="" style="cursor: pointer;" @click="updateValue">
        </div>
    </div>
</template>

<style src="../styles/search.css"></style>
