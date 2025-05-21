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
      menuVisible: false,
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
    //админка
    changePageAdmin_see_ad() {
      this.$router.push("/admin_see_ad");
    },
    changePageAdmin_list_users() {
      this.$router.push("/admin_list_users");
    },
    changePageAdmin_list_priyuts() {
      this.$router.push("/admin_list_priyuts");
    },
    changePageAdmin_list_priyut_for_moderation() {
      this.$router.push("/admin_list_priyut_for_moderation");
    },
    changePageAdmin_list_ad_for_moderation() {
      this.$router.push("/admin_list_ad_for_moderation");
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
    toggleMenu() {
      this.menuVisible = !this.menuVisible;
    },
    handleOption(option) {
      alert(`Вы выбрали: ${option}`);
      this.menuVisible = false;
    },
    handleClickOutside(event) {
      if (!this.$el.contains(event.target)) {
        this.menuVisible = false;
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
    document.addEventListener("click", this.handleClickOutside);
  },

  unmounted() {
    document.removeEventListener("click", this.handleClickOutside);
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <div class="adminbroni_all">
    <div class="bgr_adminbroni_cats">
      <p class="text_broni"><b> Список пользователей </b></p>
      <div class="search-bar">
        <input type="text" v-model="query" placeholder="Поиск..." />
        <button @click="search">
          <img src="../assets/imgs/Search.svg" />
        </button>
      </div>
      <!-- <div class="bgr_bronicats-container" v-if="!load">
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
      </div> -->
      <div class="rectangle1">
        <div class="rectangle2_user">
          <div class="charact_users">
            <div class="div_listpriyut1">
            <div class="div_lp1">
            <p> Пользователь </p>
            </div>
            <p class="name_lp"> Любимчики, +7 (903) 666 55 44 </p>
          </div>
          <div class="div_listpriyut1">
            <div class="div_lp2">
            <p> Статус собеседования </p>
            </div>
            <div class="status_lp_good">
              <p class="name_lp"> Пройдено </p>
            </div>
          </div>
          <div class="div_listpriyut1">
            <div class="div_lp3">
            <p> Избранное </p>
            </div>
            <p class="name_lp"> 7 </p>
            <img src="../assets/imgs/Externallink2.svg">
          </div>
          <div class="div_listpriyut1">
            <div class="div_lp3">
            <p> Брони </p>
            </div>
            <p class="name_lp"> 7 </p>
            <img src="../assets/imgs/Externallink2.svg">
          </div>
          </div>
          <div class="lp_wrapper">
          <div class="lp_menu" @click="toggleMenu">
            <p> . . . </p>
          </div>
          <div
            class="lp_dropdown"
            v-show="menuVisible"
            @click.stop
          >
            <div class="lp_option" @click="handleOption('Разрешить попытку')">Разрешить попытку</div>
            <div class="lp_option" @click="handleOption('Зачесть попытку')">Зачесть попытку</div>
            <div class="lp_option" @click="handleOption('Бан навсегда')">Бан навсегда</div>
            <div class="lp_option" @click="handleOption('Разблокировать')">Разблокировать</div>
            <div class="lp_option" @click="handleOption('Сбросить тест')">Сбросить тест</div>
          </div>
        </div>
          
        </div>
      </div>
      <div class="loader" v-if="load">
        <img src="../assets/imgs/Loader.svg" alt="" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.lp_wrapper {
  position: relative;
  display: inline-block;
}

.lp_menu {
  background-color: #FFEAD4;
  border-radius: 11px;
  height: 44px;
  width: 57px;
  font-size: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  margin: 5px 5px 0 0;
  user-select: none;
}

.lp_dropdown {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: #FFEAD4;
  border-radius: 11px;
  width: 261px;
  height: 175px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 10;
  padding: 10px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.lp_option {
  padding: 8px 20px;
  cursor: pointer;
  transition: background-color 0.2s;
  font-size: 16px;
}

.lp_option:hover {
  background-color: #DCC5AC;
}
</style>

<style src="../styles/style.css"></style>
