<script>
import { get_interview_status, update_profile, send_priyut_form } from "@/API";
import axios from 'axios';
import CatCard from "../components/CatCard.vue";

export default {
  data() {
    return {
      token: "",
      name: "",
      last_name: "",
      phone: "",
      load: false,
      login: false,
      shelterData: {
        name: "",
        town: "",
        address: "",
        phone_number: "",
        description: "",
        link_maps: ""
      },
      photoFile: null,
      fileInputKey: 0
    };
  },
  components: {
    CatCard,
  },
  methods: {
    openModal(catId) {
      this.activeModalId = catId;
    },
    closeModal(e) {
      if (!e.target.closest(".menu-modal-btn")) {
        this.activeModalId = null;
      }
    },
    isModalOpen(catId) {
      return this.activeModalId === catId;
    },
    changeTab() {
      this.$router.push(`/home`);
    },
    handleFileUpload(event) {
      this.photoFile = event.target.files[0];
    },
    async saveChanges() {
      this.load = true;
      try {
        const formData = new FormData();
        
        // Создаем JSON часть с данными приюта
        const applicationData = {
          name: this.shelterData.name,
          town: this.shelterData.town,
          address: this.shelterData.address,
          phone_number: this.shelterData.phone_number,
          description: this.shelterData.description,
          link_maps: this.shelterData.link_maps
        };
        
        // Добавляем данные в форму как JSON строку
        formData.append('application', JSON.stringify(applicationData));
        
        // Добавляем файл фото, если он есть
        if (this.photoFile) {
          formData.append('photo', this.photoFile);
        }
        console.log(this.photoFile)
        const response = await send_priyut_form(formData, this.token);
        
        console.log('Успешный ответ:', response.data);
        // Можно добавить уведомление об успехе
        this.fileInputKey++; // Сбрасываем input file
        
      } catch (error) {
        console.error('Ошибка при отправке:', error.response?.data || error.message);
        // Обработка ошибки
      } finally {
        this.load = false;
      }
    },
    fix(str) {
      return str ? str[0] : "";
    },  
    async sendChanges() {
      this.load = true;
      try {
        const reg = await update_profile(this.name, this.last_name, this.phone, this.token);
        if(reg != 401 && typeof reg != 'undefined'){
          localStorage.setItem("name", this.name);
          localStorage.setItem("last_name", this.last_name);
          localStorage.setItem("phone", this.phone);
        }
        this.load = false;
      } catch {
        this.load = false;
      }
    },
    logout() {
      this.token = '';
      this.name = '';
      this.last_name = '';
      localStorage.setItem('token', '');
      localStorage.setItem('name', '');
      localStorage.setItem('last_name', '');
      this.$router.push("/home");
    }
  },
  async mounted() {
    this.token = localStorage.getItem("token");
    if (this.token && this.token != "") {
      this.name = localStorage.getItem("name");
      this.last_name = localStorage.getItem("last_name");
      this.phone = localStorage.getItem("phone");
      const json = await get_interview_status(this.token);
      if(json == 401 || typeof json == 'undefined'){
        localStorage.setItem("token", ''); 
        this.login = false;
      } else {
        this.login = true;
        // Здесь можно добавить загрузку текущих данных приюта
        // await this.loadShelterData();
      }
    }
    document.addEventListener("click", this.closeModal.bind(this));
  },
  unmounted() {
    document.removeEventListener("click", this.closeModal.bind(this));
  }
};
</script>

<template>
  <div class="background_profile_right"> 
    <div class="status_sobes" v-if="!load"> <p> Мой приют </p> </div>
    <div class="priyut-change" v-if="!load">
      <!-- Поле загрузки изображения -->
      <div class="file-upload-container">
        <label class="file-upload-label">
          <input
            type="file"
            @change="handleFileUpload"
            accept="image/*"
            :key="fileInputKey"
            class="file-upload-input"
          />
          <span>{{ photoFile ? photoFile.name : 'Загрузить фото приюта' }}</span>
        </label>
      </div>

      <p>Название приюта</p>
      <label class="input">
        <input
          v-model="shelterData.name"
          class="input__field"
          type="text"
          placeholder=" "
        />
        <span class="input__label">Например: Happy Paws Shelter</span>
      </label>

      <p>Город</p>
      <label class="input">
        <input
          v-model="shelterData.town"
          class="input__field"
          type="text"
          placeholder=" "
        />
        <span class="input__label">Например: Москва</span>
      </label>

      <p>Адрес</p>
      <label class="input">
        <input
          v-model="shelterData.address"
          class="input__field"
          type="text"
          placeholder=" "
        />
        <span class="input__label">Например: ул. Ленина, д. 10</span>
      </label>

      <p>Телефон</p>
      <label class="input">
        <input
          v-model="shelterData.phone_number"
          class="input__field"
          type="text"
          placeholder=" "
        />
        <span class="input__label">Например: +79991234567</span>
      </label>

      <div class="custom-input3-conteiner">
        <p>Описание</p>
        <textarea 
          v-model="shelterData.description" 
          class="custom-input3 custom-input3-small"
          placeholder="Описание приюта"
        ></textarea>
      </div>

      <p>Ссылка на карты</p>
      <label class="input">
        <input
          v-model="shelterData.link_maps"
          class="input__field"
          type="text"
          placeholder=" "
        />
        <span class="input__label">Например: https://maps.example.com/happy-paws</span>
      </label>
    </div>
    
    <div class="status_sobes" v-if="!load" @click="saveChanges">
      <p>Сохранить изменения</p>
    </div>
    
    <div class="loader" v-if="load">
      <img src="../assets/imgs/Loader.svg" alt="Загрузка" />
    </div>   
  </div>
</template>

<style scoped>
.file-upload-container {
  margin-bottom: 20px;
}

.file-upload-label {
  display: inline-block;
  padding: 10px 15px;
  background-color: #FFEEE0;
  border-radius: 11px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.file-upload-label:hover {
  background-color: #DFBB9E;
}

.file-upload-input {
  display: none;
}

</style>