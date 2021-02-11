<template>
    <div>
        <h2>Log In</h2>
        <form @submit.prevent="handleSubmit">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" 
                    v-model="username" 
                    name="username" 
                    class="form-control" 
                    :class="{'is-invalid'
                    :submitted && !username}" 
                />
                <div v-if="submitted && !username" 
                    class="invalid-feedback">
                    Username is required
                </div>

            </div>
            <div class="form-group">
                <label htmlFor="password">Password</label>
                <input type="password" 
                    v-model="password" 
                    name="password" 
                    class="form-control" 
                    :class="{'is-invalid'
                    :submitted && !password}" 
                />
                <div v-if="submitted && !password" 
                    class="invalid-feedback">
                    Password is required
                </div>
            </div>
            <div class="form-group">
                <button class="btn btn-primary" 
                    :disabled="loggingIn">
                    Log In
                </button>
                <i v-if="loggingIn" 
                    class="fa fa-circle-o-notch fa-spin fa-3x fa-fw">
                </i>
            </div>
        </form>
        <div v-if="loginError" class="alert alert-danger">
            Username: test
            Password: test
        </div>
    </div>
</template>

<script>


export default {
    name: 'LogIn',
  
    data() {
        return {
            username: '',
            password: '',
            submitted: false,
            loginError: '',
            loggingIn: false
        };
    },

    mounted: function() {   
        this.$eventBus.$on('USER_LOGGED_IN', () => {
            this.$router.push('/dashboard');
        });
        this.$eventBus.$on('INCORRECT_CREDENTIALS', () => {
            this.submitted = false;
            this.loggingIn = false;
            this.$swal('Credentials are not valid');
        });

    
  },
 
    methods: {
        handleSubmit () {
            this.submitted = true;
            //if no username or password, return
            if (!this.username || !this.password) {
                return;
            }
            this.loggingIn = true;
            this.$auth.login(this.username, this.password);
        }
    }
};
</script>

<style>

</style>