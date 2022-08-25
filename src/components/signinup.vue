<template>

  <link rel="stylesheet" href="../static/signup.css">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
	<link rel="stylesheet" href="/static/img_home.css">
  <link rel="stylesheet" href="/static/nav_bar.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">


<div class="login-wrap">
	<div class="login-html">
		<input id="tab-1" type="radio" name="tab" class="sign-in" checked><label for="tab-1" class="tab" >Sign In</label>
		<input id="tab-2" type="radio" name="tab" class="sign-up"><label for="tab-2" class="tab">Sign Up</label>
		<div class="login-form">
			<div class="sign-in-htm">
        <p style="color:greenyellow;" v-if="$store.state.session">Your session expired. Kindly login again!!</p>
         <p style="color: red; text-underline: black" v-if="error_login">Incorrect Username/Password. Please try again</p>

				<form id="sign-in-form" @submit.prevent>
				<div class="group">
					<label for="userSI" class="label">Username</label>
					<input id="userSI" type="text" class="input" v-model="si_un" required>
				</div>
				<div class="group">
					<label for="passSI" class="label">Password</label>
					<input id="passSI" type="password" class="input" data-type="password" v-model="si_ps" required>
				</div>

				<div class="group">
          <button type="submit" class="button"  @click="signinCall" >Sign In</button>
				</div>
				<div class="hr"></div>
				<div class="foot-lnk">
				</div>
			</form>


			</div>

			<form action="/signin-up/" method="POST" id="sign-up-form" @submit.prevent>
			<div class="sign-up-htm">
        <p style="color: red; text-underline: black" v-if="error_signup">Something went wrong while signing you up. Please try again</p>
				<div class="group">
					<label for="userSU" class="label">Username</label>
					<input id="userSU" type="text" class="input" v-model="su_un" required>
				</div>
				<div class="group">
					<label for="passSU" class="label">Password</label>
					<input id="passSU" type="password" @input="checkPassword" class="input" v-model="su_ps" autocomplete="off" placeholder="Password" required/>
<!--          <input id="passSU" type="password" class="input" data-type="password" v-model="su_ps" required>-->

				</div>

				<div class="group">
					<label for="email" class="label">Email Address</label>
					<input id="email" type="text" class="input" v-model="su_email" required>
				</div>

        <!-- okokokok      -->
        <div>
          <div class="input_container">
		<ul>
			<li v-bind:class="{ is_valid: contains_eight_characters }">8 Characters</li>
			<li v-bind:class="{ is_valid: contains_number }">Contains Number</li>
			<li v-bind:class="{ is_valid: contains_uppercase }">Contains Uppercase</li>
			<li v-bind:class="{ is_valid: contains_special_character }">Contains Special Character</li>
		</ul>

		<div class="checkmark_container" v-bind:class="{ show_checkmark: valid_password }">
			<svg width="50%" height="50%" viewBox="0 0 140 100">
				<path class="checkmark" v-bind:class="{ checked: valid_password }" d="M10,50 l25,40 l95,-70" />
			</svg>
		</div>

	</div>
        </div>
        <!-- okokokok				-->
        <br>
        <div class="group">
          <template v-if="valid_password == false">
            <button type="submit" class="button btn btn-danger" style="background-color: red" disabled>Sign up</button>
            </template>
					<template v-else>
            <button type="submit" class="button" @click="signupCall">Sign Up</button>
            </template>
				</div>

			</div>
			</form>
		</div>
	</div>
</div>



</template>


<script>
export default {
  name: "signinup",
  data(){
    return{
      si_un : "",
      si_ps : "",
      su_un : "",
      su_ps : "",
      su_email: "",
      error_login: false,
      error_signup: false,
      // -------
      password: null,
      password_length: 0,
		  contains_eight_characters: false,
      contains_number: false,
      contains_uppercase: false,
		  contains_special_character: false,
      valid_password: false
    }
  },


  methods : {
    signinCall: function () {
      if(this.si_un.trim() !== "" && this.si_ps.trim() !== ""){
      fetch(this.$store.state.base_url + "/login/", {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "username": this.si_un,
          "password": this.si_ps
        })
      }).then(resp => resp.json())
          .then(data => {
            if (data.access_token != "Failed") {
              localStorage.access_token = data.access_token;
              localStorage.username = this.si_un;
              localStorage.login = true;
              this.$store.commit('loginUser', this.si_un)
              this.$router.push({name: 'Dashboard'})
            } else {
              this.error_login = true;
              //window.alert("Failed to login. Did you check the username/password?")
            }
          })
        }


    },


    signupCall: function () {
      if (this.su_un.trim() !== "") {
        fetch(this.$store.state.base_url + "/signup/", {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "username": this.su_un,
            "password": this.su_ps,
            "email": this.su_email
          })
        }).then(resp => resp.json())
            .then(data => {
                  console.log("data : ", data)
                  if (data.signup == "Successful") {
                    let msg_to_send = `A new user with the username ${this.su_un} and email ${this.su_email} has registered on your platform. Congratulations!`

                    fetch("https://chat.googleapis.com/v1/spaces/AAAAYUcZwmE/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=JRwfxb7q6Vdbciod2gALNcYPMO9MdLTDqRHsEmMU13k%3D", {
                      method: "POST",
                      headers: {
                        'Content-Type': 'application/json'
                      },
                      body: JSON.stringify({'text': msg_to_send})
                    }).then(resp => {
                      if(resp.ok) return resp.json()
                      else throw new Error()
                    }).then(data => console.log(data))
                      .catch(e => console.log("AN ERROR OCCURRED WITH SSE--->", e))

                    this.error_signup = false
                    let confirm = window.confirm("Sign-up successful. would you like to login?")
                    if (confirm) {
                      this.si_un = this.su_un;
                      this.si_ps = this.su_ps;
                      this.signinCall();

                    }
                  } else {
                    this.error_signup = true;
                  }
                }
            ).catch(e => {
          this.error_signup = true;
          console.log("error : ", e)
        })
      } else {
        window.alert("Username Can't be empty!!")
      }

    },

  },
  computed: {
    checkPassword: function() {
      this.password_length = this.su_ps.length;
			const format = /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;

      if (this.password_length >= 8) {
        this.contains_eight_characters = true;
      } else {
        this.contains_eight_characters = false;
			}

      this.contains_number = /\d/.test(this.su_ps);
      this.contains_uppercase = /[A-Z]/.test(this.su_ps);
			this.contains_special_character = format.test(this.su_ps);

      if (this.contains_eight_characters === true &&
					this.contains_special_character === true &&
					this.contains_uppercase === true &&
					this.contains_number === true &&
          this.su_un.trim() !== "") {
						this.valid_password = true;
      } else {
        this.valid_password = false;
      }
    }

  },
  beforeMount() {
    if(localStorage.login == 'true'){
     this.$router.push({name:"Dashboard"})
    };
  }
}
</script>

<style scoped>

        .btn-outline-success:hover{
            background-color: #46b8da !important;
        }
        .btn-outline-success{
            color: #46b8da;
            border: #46b8da;
        }

        /* Basic Config --------- */

html { box-sizing: border-box; }

*, *:before, *:after { box-sizing: inherit; }

html, body {
	height: 100%;
	width: 100%;
	margin: 0;
	padding: 0;
}

body {
	font-family: 'Open Sans', sans-serif;
	display: flex;
	justify-content: center;
	align-items: center;
	background: #ff6b6b;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
}

h2 {
	text-align: center;
	color: #FFF;
	font-weight: 400;
}

ul {
	padding-left: 20px;
	display: flex;
	flex-direction: column;
	align-items: flex-start;
}

li {
	margin-bottom: 8px;
	color: #525f7f;
	position: relative;
}

li:before {
  content: "";
	width: 0%; height: 2px;
	background: #2ecc71;
	position: absolute;
	left: 0; top: 50%;
	display: block;
	transition: all .6s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

#app { width: 400px; }


/* Password Input --------- */

.input_container {
	position: relative;
	padding: 30px;
	box-shadow: 0 10px 20px rgba(0,0,0,0.19), 0 6px 6px rgba(0,0,0,0.23);
	border-radius: 6px;
	background: #FFF;
}

input[type="password"] {
	line-height: 1.5;
	display: block;
	color: rgba(136, 152, 170, 1);
	font-weight: 300;
	width: 100%;
	height: calc(2.75rem + 2px);
	padding: .625rem .75rem;
	border-radius: .25rem;
	background-color: #fff;
	transition: border-color .4s ease;
	border: 1px solid #cad1d7;
	outline: 0;
}

input[type="password"]:focus {
	border-color: rgba(50, 151, 211, .45);
}


/* Checkmark & Strikethrough --------- */

.is_valid { color: rgba(136, 152, 170, 0.8); }
.is_valid:before { width: 100%; }

.checkmark_container {
	border-radius: 50%;
	position: absolute;
	top: -15px; right: -15px;
	background: #2ecc71;
	width: 50px; height: 50px;
	visibility: hidden;
	opacity: 0;
	display: flex;
	justify-content: center;
	align-items: center;
	transition: opacity .4s ease;
}

.show_checkmark {
  visibility: visible;
  opacity: 1;
}

.checkmark {
  width: 100%;
  height: 100%;
  fill: none;
  stroke: white;
  stroke-width: 15;
  stroke-linecap: round;
  stroke-dasharray: 180;
  stroke-dashoffset: 180;
}

.checked { animation: draw 0.5s ease forwards; }

@keyframes draw {
  to { stroke-dashoffset: 0; }
}



</style>