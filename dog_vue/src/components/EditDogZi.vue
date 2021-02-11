<template>
    <div class="mt-4">
        <div>
        <h3>Dog Details</h3>
        </div>
        <div class="mt-4 mb-4">
            <div v-if="details.adoptability_status == 'Available'">
                <button 
                    @click="AddAdoption()" 
                    type="button" 
                    class="btn btn-sm btn-primary btn-block"
                    >Add Adoption
                </button>
            </div>
        </div> 

         <div>
            <table class="table table-hover">
                <thead>
                <tr>
                    <th>Dog ID</th>
                    <th>Name</th>
                    <th>Breed</th>
                    <th>Sex</th>
                    <th>Alteration Status</th>
                    <th>DOB</th>
                    <th>Microchip ID</th>
                    <th>Surrender Reason</th>
                    <th>Surrender Date</th>
                    <th>Surrendered by Animal Control</th>
                    <th>Adoptability Status</th>
                    <th>Description</th>
                </tr>
                </thead>
                <tbody v-if="details">
                    <td>{{details.dog_ID}}</td>
                    <td>{{details.dog_name}}</td>
                    <!-- <td v-if="details.breed !=  null"> -->
                    <td> {{details.breed}}</td>
                    
                    <td>{{details.sex}}</td>
                  
                    <td>{{details.alteration_status}} </td>
                    
                    <td>{{details.date_of_birth}}</td>
                    <td>{{details.microchip_ID}}</td>
                    
                    <td>{{details.surrender_reason}}</td>
                    <td>{{details.surrender_date}}</td>
                    <td>{{details.surrendered_by_animal_control}}</td>
                    <td>{{details.adoptability_status}}</td>
                    <td>{{details.description}}</td>
                </tbody>
            </table>
         </div>
    
     <div v-if="details.breed == ('Unknown' ||''|| 'Mixed')">
        <label for="dogbreed"><b>Dog Breed</b></label>
        <el-select v-model="new_breed" multiple placeholder="Select Breed" @change="selectModel($event)">
            <el-option
            v-for="item in optionList"
            :key="item.value"
            :label="item.label"
            :value="item.value"> {{item.value}}
            </el-option>
        </el-select>
     </div>
        
              <div v-if="details.sex == 'Unknown'">
                  <label for="sex"><b>Dog Sex</b></label>
                    <select v-model="new_sex">
                        <option value="Unknown">Unknown</option>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                        </select>
                </div>
       
        <div v-if="details.alteration_status == 0">
            <label for="alteration_status"><b>Alteration Status</b></label>
                        <select v-model="new_alteration_status">
                            <option selected value="0">No</option>
                            <option value="1">Yes</option>
                        </select>
                    </div>
       
        <div v-if="details.microchip_ID == null">
             <label for="dog_microchip"><b>Microchip ID</b></label>
                    <input type="text" v-model="new_microchip_ID">
                    </div>

        <div class="mb-4" v-if="details.adoptability_status != 'Available'">
            <button 
                @click="onSubmit"
                type="button" 
                class="btn btn-sm btn-secondary btn-block"
                >Update Dog Info
            </button>
        </div>
        <div>
            <h3>Expenses</h3>
                <table class="table table-hover">
                    <tbody>
                    <tr>
                        <th>Dog ID</th>
                        <th>Expense Date</th>
                        <th>Vendor</th>
                        <th>Amount</th>
                        <th>Description</th>
                    </tr>

                    <tr v-for="(exp, index) in dogExpenses" :key="index">
                        <td>{{exp.dog_ID}}</td>
                        <td>{{exp.expense_date}}</td>
                        <td>{{exp.vendor_name}}</td>
                        <td>{{exp.amount}}</td>
                        <td>{{exp.description}}</td>
                    </tr>
                    </tbody>
                </table>
        </div>
        <div class="mb-4">
            <button 
                @click="AddExpense()"
                type="button" 
                class="btn btn-sm btn-secondary"
                >Add New Expense
            </button>
        </div>
    </div>
</template>


<script>
    export default {
    name: 'DogIndex',
    
    data () {
        return {
            new_sex: '',
            new_alteration_status: 0,
            new_microchip_ID: '',
            new_breed: [],
            selectedDog: '',
            details: [],
            dogExpenses: [],
            optionList: []
        }
    },

    mounted: function() {
        if (typeof this.$route.params.dogID != 'undefined'){
        this.selectedDog = this.$route.params.dogID;
        this.getDog();
        this.getDogExpenses();
    }
  },

    methods:{
        getBreed: function() {
            
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
    
        getDog: function() {

            var url = "http://127.0.0.1:5000/api/dogindex/" + this.selectedDog;

            var yourConfig = {
                headers: {
                "Content-Type": "application/json",
                "Authorization": "JWT " + this.$auth.getAccessToken()
                }
            }

            this.$axios
            .get(url, yourConfig)
            .then(response => {
                if ((typeof response == 'undefined') 
                || (typeof response.data == 'undefined')
                || (typeof response.data.dog_ID == 'undefined')
                ){
                this.$swal('Something went wrong, please try again later.');
                return;
                }

                this.details = response.data;

            })
            .catch((error) => {
                if(error.response.status == 404) {
                this.$swal('Something went wrong, please try again later.');
                }
            })
        },
    
        getDogExpenses: function() {

            var url = 'http://127.0.0.1:5000/api/expense/' + this.selectedDog;
            var yourConfig = {
                headers: {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + this.$auth.getAccessToken()
                }
            } 
            this.dogExpenses = [];     

            this.$axios
            .get(url, yourConfig)
            .then((response) => {
                if (typeof response.data.dog_ID != 'undefined') {
                this.dogExpenses.push(response.data);
                } else {
                    for (var i = 0; i < response.data.length; i++) {
                    this.dogExpenses.push(response.data[i]);
                    }
                }
            })
        },

        onSubmit() {
//            if ((this.new_alteration_status == this.details.alteration_status)
//                || (this.new_alteration_status == 0) || (this.new_alteration_status == 'No')
//                || (this.new_microchip_ID == this.details.microchip_ID)
//                || (this.new_microchip_ID == '') || (this.new_microchip_ID == null)
//                || (!this.new_microchip_ID)
//                || (this.new_sex == this.details.sex)
//                || (this.new_breed == this.details.breed)) {
//
//                this.$swal("You must edit an item to update details.");
//                return;
//            }
            let data = {
                "dog_ID": this.selectedDog, 
                "breed": this.new_breed, 
                "sex": this.new_sex, 
                "alteration_status": this.new_alteration_status,
                "microchip_ID": this.new_microchip_ID,
                "email_address": this.$auth.getUsername()
            }

            var url = 'http://127.0.0.1:5000/api/edit_dog/'+ this.selectedDog;
            var yourConfig = {
                headers: {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + this.$auth.getAccessToken()
                }
            }        
            this.$axios
            .put(url, data, yourConfig)
            .then((response)=> {
                console.log(response);
                this.$swal("Dog information has been updated.");
                this.$router.push('/dashboard');

            })
            .catch(function(error){
                console.log(error);
                this.$swal("Something went wrong. Please try again later.")
            })
        },

        AddAdoption() {
            this.$router.push('/dashboard/dog-detail/adoption');
        },

        AddExpense() {
            this.$router.push('/dashboard/dog-detail/add-expense/'+ this.details.dog_ID);

        }
    },

   created(){
       this.getBreed();
    }
}
</script>

<style lang="scss" scoped>
</style>
