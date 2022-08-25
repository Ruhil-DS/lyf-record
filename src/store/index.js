import { createStore } from 'vuex'

export default createStore({
  state: {
    base_url : "http://127.0.0.1:5000/api",
    login: false,
    user: 'pushpak',
    session: false
  },
  getters: {
  },
  mutations: {
    loginUser : function (state, username){
      state.user = username;
      state.login = true;
    }
  },
  actions: {
  },
  modules: {
  }
})


