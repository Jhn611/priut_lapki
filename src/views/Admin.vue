<script>
import { get_book_cats, search_book_cats, unbind_cat } from "@/API";
import CatCard from "../components/CatCard.vue";
export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      token: "",
      name: "",
      last_name: "",
      cats: [],
      query: "",
      load: false,
    };
  },
  components: {
    //тут импортируются компоненты (например карточка)
    CatCard,
  },
  computed: {
    // тут функции которые что-то считают и возвращают что-то (пока можно не использовать, это для оптимизации)
  },
  methods: {
    changePageToProfile() {
      this.$router.push("/profile");
    },
    changePageToHome() {
      this.$router.push("/home");
    },
    changePageToSaved() {
      this.$router.push("/saved");
    },
    changePageToContacts() {
      this.$router.push("/contacts");
    },
    changePageToHowtohelp() {
      this.$router.push("/howtohelp");
    },
    changePageAdmin() {
      this.$router.push("/admin");
    },
    async loadBookedCats() {
      this.load = true;
      try {
        const reg = await get_book_cats(this.token);
        if (typeof reg != "number" && typeof reg != "undefined") {
          console.log(reg, typeof reg);
          this.cats = reg;
        }
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    async search() {
      this.load = true;
      try {
        const reg = await search_book_cats(this.query, this.token);
        if (typeof reg != "number" && typeof reg != "undefined") {
          console.log(reg, typeof reg);
          this.cats = reg;
        }
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    async unbind(cat) {
      this.load = true;
      try {
        const reg = await unbind_cat(cat, this.token);
        this.loadBookedCats();
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
  },

  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.name = localStorage.getItem("name");
      this.last_name = localStorage.getItem("last_name");
      await this.loadBookedCats();
    }
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="adminbroni_all">
    <div class="bgr_adminbroni_cats">
      <p class="text_broni"><b> Список броней </b></p>
      <div class="search-bar">
        <input type="text" v-model="query" placeholder="Поиск..." />
        <button @click="search">
          <img src="../assets/imgs/Search.svg" />
        </button>
      </div>
      <div class="bgr_bronicats-container" v-if="!load">
        <div class="bgr_bronicats" v-for="item in cats" :key="item">
          <div class="photo_cat">
            <img
              class="photo_cat-img"
              :src="`http://26.48.41.80:8000/static/photos/${item.cat.photo_url}`"
              alt=""
            />
          </div>
          <div class="data_broni">
            <div class="all_bgr_imya">
              <div class="bgr_imya">
                <p class="p_imya">Имя кошки</p>
                <div class="bgr_imya_cat">
                  <p class="p_imya_cat">{{ item.cat.name }}</p>
                </div>
              </div>
            </div>

            <div class="bgr_imya">
              <p class="p_imya">Имя клиента</p>
              <div class="bgr_imya_cat">
                <p class="p_imya_cat">{{ item.user.first_name }}</p>
              </div>
            </div>
            <div class="bgr_imya">
              <p class="p_imya">Номер телефона</p>
              <div class="bgr_imya_cat">
                <p class="p_imya_cat">{{ item.user.phone_number }}</p>
              </div>
            </div>
          </div>
          <div class="button_krest" @click="unbind(item.cat.id)"><img src="../assets/imgs/krest.svg" /></div>
        </div>
      </div>
      <div class="loader" v-if="load">
        <img src="../assets/imgs/Loader.svg" alt="" />
      </div>
    </div>
  </div>
</template>

<style src="../styles/style.css"></style>
