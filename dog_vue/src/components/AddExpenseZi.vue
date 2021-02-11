/* eslint-disable */
<template>
  <div class="mt-4">
    <h2>Add Expense</h2>
    <div class="mt-4">
      <span class="text-secondary">Add an expense for Dog ID: </span>
      <span class="font-weight-bold text-primary"> {{this.cur_dog_ID}}</span>
    </div>
    <form class="container">
      <div class="input-group align-items-center mt-4">
        <span class="font-weight-bold">Expense Date:</span><pre> </pre>
        <input
          v-model="expense_date"
          type="date"
          class="form-control"
          required
        >
        <pre> </pre>
        <span class="font-weight-bold">Vendor Name:</span><pre> </pre>
        <input
          v-model="vendor_name"
          type="text"
          class="form-control"
          required
        >
      <pre> </pre>
        <span class="font-weight-bold">$ Amount:</span><pre> </pre>
        <input
          v-model.number="amount"
          type="text"
          class="form-control"
          required
        >
      <pre> </pre>
      </div>
      <div class="input-group align-items-center mt-4">
        <span class="font-weight-bold">Description:</span><pre> </pre>
        <textarea
          v-model="description"
          type="text"
          class="form-control"
          placeholder="Add optional description ..."
        >
        <pre> </pre>
        </textarea>
      </div>
      <div class="mt-4">
        <button 
          @click="onSubmit" 
          type="button" 
          class="btn btn-sm btn-secondary"
          >Submit
        </button>
      </div>
    </form>
  </div>
</template>

<style lang="scss" scoped>
</style>

<script>

export default {
  name: 'AddExpense',
  data(){
    return{
      cur_dog_ID: String(this.$route.path).replace(/^.*\/(.*)$/, "$1"),
      expense_date: null,
      vendor_name: null,
      amount: null,
      description: null,
      useremail: localStorage.getItem('useremail')
    }
  },
  mounted: function() {
    this.getExpenses();
  },
  methods: {
      getExpenses: function() {

        var urlExp = 'http://127.0.0.1:5000/api/expense/' + this.cur_dog_ID;
        var yourConfigExp = {
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.$auth.getAccessToken()
            }
        }
        this.$axios
        .get(urlExp, yourConfigExp)
        .then((response)=> {
            this.details = response.data;
        })
        .catch(function(error){
            console.log(error);
        })

      },

      onSubmit() {
        if ((this.expense_date == '' || !this.expense_date)
        || (this.vendor_name == '' || !this.vendor_name)
        || (this.amount == '' || !this.amount)
      ) {
       this.$swal('Date, vendor name, and amount are required fields.');
       return;
      }

        let data = {dog_ID: this.cur_dog_ID,
            expense_date: this.expense_date, 
            vendor_name: this.vendor_name,
            amount: this.amount,
            description: this.description,
        }
        for (let i =0; i< this.details.length; i++) {
           if ((this.details[i].expense_date == this.expense_date
              && this.details[i].vendor_name == this.vendor_name
              && this.details[i].amount == this.amount)
            ){
                this.$swal('No duplicate values allowed.');
                return;
              }
        }
       

        var url = 'http://127.0.0.1:5000/api/expense/' + this.cur_dog_ID;
        var yourConfig = {
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.$auth.getAccessToken()
            }
        }
        this.$axios
        .post(url, data, yourConfig)
        .then((response)=> {
            this.details = response.data;

            this.$swal('Expense has been added.');

            this.$router.push('/dashboard');
            
        })
        .catch(function(error){
          console.log(error);
            this.$swal('No duplicate values allowed.');
        })
      }
  },
}
</script>