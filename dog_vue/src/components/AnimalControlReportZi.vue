<template>
    <div class="mt-4 mb-5">
        <h3>Animal Control Report</h3>
         <div>
            <table class="table table-hover mt-4">
                <thead>
                <tr>
                    <th>Month</th>
                    <th>Dogs Surrendered</th>
                    <th>Expenses</th>
                    <th>Adopted, In Shelter > 60 days</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="item in searchResult" 
                    v-bind:key="item.year_month">
                    <td><a :href="'/dashboard/animal-control-report-details/'+ item.year_month">{{item.year_month}}</a></td>
                    <td>{{item.monthly_summary[0]}}</td>
                    <td>{{item.monthly_summary[2]}}</td>
                    <td>{{item.monthly_summary[1]}}</td>
                </tr>
                </tbody>
            </table>
         </div>
    </div>
</template>

<style lang="scss" scoped>
</style>

<script>
import axios from 'axios'
export default {
  name: 'AnimalControlReport',
  
  data () {
      return {
        searchResult: [],
        isAdmin : 0,
      }
  },
  methods:{
    display(){
        var url = 'http://127.0.0.1:5000/api/reports/animal_control_report';
        var yourConfig = {
            headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.$auth.getAccessToken()
            }
        }
        axios.get(url, yourConfig).then((res) => {
            console.log("in animal_control_report() res.data is:", res.data)
            this.searchResult = res.data
        })   
    },
  },
    created(){
            console.log("in dashborad created()")
            this.display()
    }
}
</script>