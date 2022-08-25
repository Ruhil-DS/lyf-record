<template>
 <!-- OFF-CANVAS NAV BAR-->
  <template v-if="nav_flag == false">
  <nav class="bg-dark" style="color: #38b6ff" >
    <div class="offcanvas offcanvas-start bg-dark" id="nav_left">
  <div class="offcanvas-header">
    <h1 class="offcanvas-title" style="font-family: 'ui-monospace'">Lyf Record</h1>
    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" ></button>
  </div>
  <div class="offcanvas-body">
    <img src="@/QuantifiedSelfApp-FLASK/static/images/logo.svg">
            <div class="container">
                <div class="d-grid gap-2 col-6 mx-auto">
                   <div class="col">
                  <span>
                  <router-link to="/">
                    <div id="len4" class="hoverable">
                      Home
                    </div></router-link>
                  </span>
                </div>

                  <div class="col">
                  <span>
                  <router-link to="/About/">
                    <div id="len2" class="hoverable">
                      About
                    </div></router-link>
                  </span>
                </div>

                <div class="col">
                  <span>
                  <router-link to="/signin-up/">
                    <div id="len3" class="hoverable">
                      SIGN&nbsp;
                    IN/UP
                    </div></router-link>
                  </span>
                </div>



                </div>
            </div>
  </div>
</div>

    <button class="btn btn-outline-primary me-2 btn-lg" type="button" data-bs-toggle="offcanvas"
        data-bs-target="#nav_left" style="width: 100%">
            <i class="fa fa-bars" style="font-size:30px"></i>
    </button>

  </nav>
  </template>

  <template v-if="nav_flag">

<!-----------START Of NAVIGATION BAR--------->
<div class="offcanvas offcanvas-start bg-dark" id="nav_left">
  <div class="offcanvas-header">
    <h1 class="offcanvas-title" style="font-family: 'ui-monospace'; color:dodgerblue">&nbsp; &nbsp;Lyf Record <img src="@/QuantifiedSelfApp-FLASK/static/images/logo.svg" width="60" height="60" align="left"></h1>
    <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas" ></button>
  </div>
  <div class="offcanvas-body">
    <img src="@/QuantifiedSelfApp-FLASK/static/images/baymax_loop.gif" width="150" height="150" align="left">
    <br>
    <div style="font-size: 45px; color: #c51313">{{$store.state.user}} !</div>

            <div class="container">
                <div class="d-grid gap-2 col-3 mx-left">
                  <br><br><br><br><br>

                  <div class="col"><span><router-link  class="hoverable" :to="{name:'Dashboard'}" :key="$route.fullPath">Dashboard</router-link></span></div>
                  <div class="col"><span><router-link class="hoverable" :to="{name:'view_trackers'}">View Trackers</router-link></span></div>
                  <div class="col"><span><router-link class="hoverable" :to="{name: 'create_tracker'}">Add Tracker</router-link></span></div>
                  <div class="col"><span><router-link class="hoverable" :to="{name: 'signout'}">Sign out</router-link></span></div>

                </div>
            </div>
  </div>
</div>

    <button class="btn btn-outline-success me-2 btn-lg " type="button" data-bs-toggle="offcanvas"
        data-bs-target="#nav_left" style="width: 100%">
            <i class="fa fa-bars" style="font-size:30px"></i>
    </button>
  </template>
</template>

<script>
export default {
  name: "navBar",
  data(){
    return {
      nav_flag: ''
    }
  },
  beforeMount() {
    if(localStorage.login=='true') this.nav_flag = true
    else this.nav_flag = false
  }
}


</script>

<style scoped>

</style>