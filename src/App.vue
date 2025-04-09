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
    changePageToSurrenderaCat() {
      this.$router.push("/surrender_a_cat");
    },
    changePageToLogRegIn() {
      this.$router.push("/auth");
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
            @click="changePageToHome"
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
        <div class="header_text1">
          <a @click="changePageToHowtohelp" style="cursor: pointer">
            Как помочь
          </a>
          <a @click="changePageToSurrenderaCat" style="cursor: pointer">
            Сдать кошку в приют
          </a>
          <a @click="changePageToContacts" style="cursor: pointer">
            Контакты
          </a>
        </div>

        <div class="header_text2">
          <a> Москва Ул. Софьи Ковалевской 228 </a>
        </div>
      </div>
    </div>
  </header>

  <main id="main">
    <RouterView :command="command" />
  </main>

  <footer class=".bgr_footer" v-if="!load">
    <div class="elements_footer">
      <div class="upper_piece">
        <div class="logo_footer">
          <img src="./assets/imgs/logo.svg" class="logo_img_footer" />
          <div class="boxes_img_footer">
            <img src="./assets/imgs/Box.svg" class="box_img_footer" />
            <img src="./assets/imgs/Box.svg" class="box_img_footer" />
            <img src="./assets/imgs/Box.svg" class="box_img_footer" />
          </div>
        </div>

        <div class="zag_pol_footer">
          <div class="zag_footer">
            <p>Информация</p>
            <p>Контакты</p>
            <p>Мы в соцсетях</p>
          </div>
          <div class="poloska1"></div>
          <div class="infos_footer">
            <div class="info1_footer">
              <p>Время работы:</p>
              <p>10:00-20:00</p>
              <p>Адрес:</p>
              <p>ул. Софьи 228</p>
            </div>

            <div class="info2_footer">
              <p>Номер телефона:</p>
              <p>+7 999 888 55 44</p>
              <p>Почта:</p>
              <p>priyut@mail.ru</p>
            </div>

            <div class="info3_footer">
              <p><a href="https://vk.com/"> Вконтакте </a></p>
              <p><a href="https://web.telegram.org/"> Telegram </a></p>
            </div>
          </div>
        </div>
      </div>

      <div class="poloska2"></div>
      <div class="p_bottom_footer">
        <p>&#169; Котоприют</p>
        <div class="p_bottom_right_footer">
          <p>Котоприют</p>
          <p>Лапочки</p>
        </div>
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
