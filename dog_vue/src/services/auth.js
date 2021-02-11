this.login = function(username, password) {
    var url = 'http://127.0.0.1:5000/auth';

    var data = {
        'username': username,
        'password': password
    }

    var config = {
        headers: {
            'Content-Type': 'application/json',
        }
    }

    this.$axios
    .post(url, data, config)
    .then(response => {
        var accessToken = response.data.access_token;
        localStorage.setItem('token', accessToken);
        localStorage.setItem('username', username);
        this.$eventBus.$emit('USER_LOGGED_IN');
    })
    .catch((error) => {
        if(error.response.status == 404) {
            console.log('The login route is not found.');
        } else if(error.response.status == 401) {
            console.log('The credentials are incorrect.');
            this.$eventBus.$emit('INCORRECT_CREDENTIALS');
        }
    })
}

this.isAdmin = function() {
    var url = 'http://127.0.0.1:5000/api/Admin';
    var config = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.getAccessToken()
        }
    }
    
    this.$axios
    .get(url, config)
    .then(response => {
        if ((typeof response.data == 'undefined')
            || (typeof response.data.Admin == 'undefined')
            || (response.data.Admin == 'False')
        ) {
            console.log('emit false');
            this.$eventBus.$emit('IS_ADMIN', false);
            return;
        }
        console.log('emit true');
        this.$eventBus.$emit('IS_ADMIN', true);
    })
    .catch((error) => {
        console.log(error);
        this.$eventBus.$emit('IS_ADMIN', false);
    })
}

this.logout = function() {
    localStorage.removeItem('token');
    this.$eventBus.$emit('USER_LOGGED_OUT');
}

this.getAccessToken = function() {
    let token = localStorage.getItem('token');
    if (typeof token != 'undefined') {
        return token;
    }
}

this.getUsername = function() {
    let username = localStorage.getItem('username');
    if (typeof username != 'undefined') {
        return username;
    }
}
