/* eslint-disable */
<template>
  <div class="mt-4">
  <h2>Add Dog Page</h2>
    <form class = "container">
      <div class="input-group align-items-center mt-4">
        <span class="font-weight-bold">Dog Name:</span><pre> </pre>
        <input
          v-model="dog_name"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">Microchip ID:</span><pre> </pre>
        <input
          v-model="dog_microchip"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">Sex:</span><pre> </pre>
        <input type="radio" id="male" value="Male" v-model="dog_sex">
        <label for="male">Male</label>
        <input type="radio" id="female" value="Female" v-model="dog_sex">
        <label for="female">Female</label>
        <input type="radio" id="unknown" name="dog_sex" value="Unknown" v-model="dog_sex">
        <label for="unknown">Unknown</label>
        <pre> </pre>

      </div>

      <br>
      <label for="alteration_status"><b>Alteration Status</b></label>
      <input type="radio" id="yes" name="alteration_status" value="1" v-model="alteration_status">
      <label for="yes">Yes</label>
      <input type="radio" id="no" name="alteration_status" value="0" v-model="alteration_status">
      <label for="no">No</label>
      <br>

      <br>
      <label for="birthday"><b>Date of birth</b></label>
      <input type="date" id="birthday" name="birthday" v-model ="birthday" >
      <br>

      <label for="surrender_date"><b>Date of surrender</b></label>
      <input type="date" id="surrender_date" name="surrender_date" v-model="surrender_date">
      <br>

      <br>
      <label for="animal_control"><b>Surrendered by animal control?</b></label>
      <input type="radio" id="yes" name="animal_control" value="1" v-model="animal_control">
      <label for="yes">Yes</label>
      <input type="radio" id="no" name="animal_control" value="0" v-model="animal_control">
      <label for="no">No</label>
      <br>

      <br>
      <label for="surrender_reason"><b>Surrender Reason</b></label><br>
      <textarea id="surrender_reason" name="surrender_reason" v-model="surrender_reason" row="2" cols="50"></textarea>
      <br>

      <br>
      <label for="description"><b>Description</b></label><br>
      <textarea id="description" name="description" v-model="description" row="20" cols="50"></textarea>
      <br>


      <div id="appselect">
      <label for="dogbreed"><b>Dog Breed</b></label>
      <el-select v-model="breedArray" multiple placeholder="Select Breed" 
        @change="selectModel($event)">
          <el-option
            v-for="item in optionList"
            :key="item.value"
            :label="item.label"
            :value="item.value"> {{item.value}}
          
          </el-option>
        </el-select>
      </div>
      <div class="mt-4">
        <button @click="submitDogInfo" 
        type="submit" 
        class="btn-sm btn-secondary"
        >Submit</button>
      </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
</style>

<script>

export default {
  name: 'AddDog',
  data(){
    return{
      dog_name: null,
      dog_sex: null,
      alteration_status: null,
      birthday: null,
      dog_microchip: null,
      surrender_date: null,
      animal_control: null,
      surrender_reason: null,
      description: null,
      adoptability_status: null,
      //for drop-down select of breed
      breedArray: [],
      optionList: [],
      useremail: localStorage.getItem('useremail'),
    }
  },
  methods: {
      getValue: function() {
          
          var url = 'http://127.0.0.1:5000/api/allbreeds';
          var yourConfig = {
              headers: {
              'Content-Type': 'application/json',
              'Authorization': 'JWT ' + this.$auth.getAccessToken()
              }
          }
          this.$axios
          .get(url, yourConfig)
          .then((response) => {
            for (var i = 0; i < response.data.length; i++) {
              this.optionList.push({
                'value': response.data[i],
                'label': response.data[i]
              })
            }
          })
      },
      submitDogInfo() {
          let data = {dog_name: this.dog_name,
            sex: this.dog_sex, 
            alteration_status: this.alteration_status,
            date_of_birth: this.birthday, 
            description: this.description, 
            microchip_ID: this.dog_microchip, 
            surrender_date: this.surrender_date,
            surrender_reason: this.surrender_reason, 
            surrendered_by_animal_control: this.animal_control, 
            adoptability_status: this.adoptability_status,
            breed: this.breedArray,  
          }
          var url = 'http://127.0.0.1:5000/api/add_dog';
          var yourConfig = {
              headers: {
              'Content-Type': 'application/json',
              'Authorization': 'JWT ' + this.$auth.getAccessToken()
              }
          }
          this.$axios
          .post(url, data, yourConfig)
          .then((response)=> {
              console.log("output in adddog: ", response)

              if (typeof response.data == 'undefined'
                || response.data != 'success'
              ) {
                this.$swal('Something went wrong, please try again later.');
                return;
              }
              
             // this.$router.push('/dashboard');

            window.location.href = '/dashboard';
              //this.$router.go('/dashboard');
              

              console.log('I am redriected');
          })
          .catch(function(error){
              console.log(error)
          })
      },
      selectModel(){
          console.log("get breedArray:", this.breedArray)
      }
  },
  created(){
     this.$eventBus.$on('LEAVING DASHBOARD', () => {
     console.log('we left dashboard');
    });
       this.getValue()
  },
}
</script>