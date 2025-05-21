<script>
import { login, register } from "./API";
import MainSearch from "./components/MainSearch.vue";

export default {
  data() {
    return {
      // тут переменные которые будут изменяться или использоваться для отображения или для изменения состояния(видно или не видно блок например)
      cats: [1, 2],
      command: "",
      login: true,
      regin: false,
      phone: null,
      password: null,
      name: null,
      last_name: null,
      token: null,
      load: false,
    };
  },
  components: {
    //тут импортируются компоненты (например карточка)
    MainSearch,
  },
  computed: {
    // тут функции которые что-то считают и возвращают что-то (пока можно не использовать, это для оптимизации)
  },
  methods: {
    //тут функции которые будем использовать для изменения визуального контента (изменение переменных, добавление стилей, и т. д.) в целом можно все тут писать
    openCard() {
      const body = document.body,
        html = document.documentElement;
      const height = Math.max(
        body.scrollHeight,
        body.offsetHeight,
        html.clientHeight,
        html.scrollHeight,
        html.offsetHeight
      );
      const pad = (window.innerWidth - 625) / 2;
      const currentStyles = document.body.style.cssText;
      document.body.style.cssText =
        currentStyles +
        `--cardpad: ${pad}px; --cardblackbgwidth: ${window.innerWidth}px; --cardblackbgheight: ${height}px`;
      console.log(pad, window.innerWidth, height);
    },
    verify() {
      this.token = localStorage.getItem("token");
      if (this.token && this.token != "") {
        this.changePageToProfile();
        this.login = true;
      } else {
        this.login = false;
        this.openCard();
      }
    },
    //header
    changePageToHellopage() {
      this.$router.push("/hellopage");
    },
    changePageToSaved() {
      this.$router.push("/saved");
    },
    changePageToProfile() {
      this.$router.push("/profile");
    },
    changePageToAnnouncements() {
      this.$router.push("/announcements");
    },
    changePageToPost_an_ad() {
      this.$router.push("/post_an_ad");
    },
    changePageToSobesedovanie() {
      this.$router.push("/sobesevodanie");
    },
    //other
    changePageToHome() {
      this.$router.push("/priyut");
    },
    changePageToLogRegIn() {
      this.$router.push("/auth");
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
    close(e) {
      if (
        !this.$el.contains(e.target) &&
        !e.target.closest(".loginBlock") &&
        !e.target.closest(".icon_user")
      ) {
        this.login = true;
      }
    },
    async LogInUser() {
      this.load = true;
      try {
        const json = await login(this.phone, this.password);
        this.token = json["access_token"];
        this.name = json["first_name"];
        this.last_name = json["last_name"];
        this.phone = json["phone_number"];
        localStorage.setItem("token", this.token);
        localStorage.setItem("name", this.name);
        localStorage.setItem("last_name", this.last_name);
        localStorage.setItem("phone", this.phone);
        location.reload();
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    async RegInUser() {
      this.load = true;
      try {
        const reg = await register(
          this.name,
          this.last_name,
          this.phone,
          this.password
        );
        if (typeof reg != "number" && typeof reg != "undefined") {
          this.LogInUser();
        }
        this.load = false;
      } catch {
        this.load = false;
      }
    },
  },
  async mounted() {
    // то что происходит когда страница создаётся (то есть запуск анимаций которые должны проиграться при открытии страницы и подобное)
    // this.$router.push("/home");
    document.addEventListener("click", this.close.bind(this));
  },

  unmounted() {
    // то что происходит когда страница закрывается/происходит переход на другу страницу
  },
};
</script>

<template>
  <header>
    <div class="background_find">
      <div class="bg_upper">
        <img
          class="logo_find"
          src="./assets/imgs/logo.svg"
          @click="changePageToHome"
          style="cursor: pointer"
        />
        <MainSearch v-model="command" />
        <div class="header_icons">
          <img
            class="icon_home"
            src="./assets/imgs/Home.svg"
            @click="changePageToHellopage"
            style="cursor: pointer"
          />
          <img
            class="icon_heart"
            src="./assets/imgs/Heart.svg"
            @click="changePageToSaved"
            style="cursor: pointer"
          />
          <img
            class="icon_user"
            src="./assets/imgs/User.svg"
            @click="verify"
            style="cursor: pointer"
          />
        </div>
      </div>
      <div class="header_text">
        <div class="header_text1" v-if="$route.path == '/admin_see_ad' || $route.path == '/admin_list_priyuts' || $route.path == '/admin_list_users' || $route.path == '/admin_list_priyut_for_moderation' || $route.path == '/admin_list_ad_for_moderation'">
          <a @click="changePageAdmin_see_ad" style="cursor: pointer">
            Просмотр объявлений
          </a>
          <a @click="changePageAdmin_list_ad_for_moderation" style="cursor: pointer">
            Модерация объявлений
          </a>
          <a @click="changePageAdmin_list_priyut_for_moderation" style="cursor: pointer">
            Модерация приютов
          </a>
          <a @click="changePageAdmin_list_users" style="cursor: pointer">
            Список пользователей
          </a>
          <a @click="changePageAdmin_list_priyuts" style="cursor: pointer">
            Список приютов
          </a>
        </div>
        <div class="header_text1" v-if="($route.path !== '/admin_see_ad') && ($route.path !== '/admin_list_priyuts') && ($route.path !== '/admin_list_users') && ($route.path !== '/admin_list_priyut_for_moderation') && ($route.path !== '/admin_list_ad_for_moderation')">
          <a @click="changePageToAnnouncements" style="cursor: pointer">
            Объявления
          </a>
          <a @click="changePageToPost_an_ad" style="cursor: pointer">
            Выложить объявление
          </a>
          <a @click="changePageToSobesedovanie" style="cursor: pointer">
            Собеседование
          </a>
        </div>
      </div>
    </div>
  </header>

  <main id="main">
    <RouterView :command="command" />
  </main>

  <footer class=".bgr_footer" v-if="!load">
    <div class="backgr_footer">
      <div class="p_footer"> 
        <p> Вместе мы сможем подарить каждому дом</p>
        <p class="p_footer2"> Нужна именно твоя помощь </p>
      </div>
    </div>
  </footer>
  <div class="black-bg" v-if="!login" @click="closeLogin">
    <div class="loginBlock">
      <div class="choose-logregin" v-if="!load">
        <p
          :class="{
            loginActive: !regin,
          }"
          @click="regin = false"
        >
          Войти
          <span
            :class="{
              loginActive: !regin,
            }"
          ></span>
        </p>
        <p
          :class="{
            loginActive: regin,
          }"
          @click="regin = true"
        >
          Зарегистрироваться
          <span
            :class="{
              loginActive: regin,
            }"
          ></span>
        </p>
      </div>
      <div class="login" v-if="!regin && !load">
        <p>Номер телефона</p>
        <label class="input">
          <input
            v-model="phone"
            class="input__field"
            type="text"
            placeholder=" "
          />
          <span class="input__label">Например: +79321112723</span>
        </label>
        <p>Пароль</p>
        <label class="input">
          <input
            v-model="password"
            class="input__field"
            type="password"
            placeholder=" "
          />
          <span class="input__label">Например: 12345678</span>
        </label>
        <div class="btn" @click="LogInUser">
          <p>Войти</p>
        </div>
      </div>
      <div class="regin" v-if="regin && !load">
        <p>Имя</p>
        <label class="input">
          <input
            v-model="name"
            class="input__field"
            type="text"
            placeholder=" "
          />
          <span class="input__label">Например: Иван</span>
        </label>

        <p>Фамилия</p>
        <label class="input">
          <input
            v-model="last_name"
            class="input__field"
            type="text"
            placeholder=" "
          />
          <span class="input__label">Например: Иванов</span>
        </label>
        <p>Номер телефона</p>
        <label class="input">
          <input
            v-model="phone"
            class="input__field"
            type="text"
            placeholder=" "
          />
          <span class="input__label">Например: +79321112723</span>
        </label>
        <p>Пароль</p>
        <label class="input">
          <input
            v-model="password"
            class="input__field"
            type="password"
            placeholder=" "
          />
          <span class="input__label">Например: 12345678</span>
        </label>
        <div class="btn" @click="RegInUser">
          <p>Зарегистрироваться</p>
        </div>
      </div>
      <div class="loader" v-if="load">
        <img src="../assets/imgs/Loader.svg" alt="" />
      </div>
    </div>
  </div>
</template>

<style src="./styles/style.css"></style>
