import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: {
      logged_in: false,
      name: null,
      email: null,
      password: null,
      _id: {
        _$oid: null
      }
    },
    tokens: {
      access: null,
      refresh: null
    }
  },
  mutations: {
    login (state, user) {
      state.user.name = user.name;
      state.user.email = user.email;
      state.user._id._$oid = user._id._$oid;
      state.user.logged_in = true;
    },
    setToken (state, tokens) {
      state.tokens.access = tokens.access,
      state.tokens.refresh = tokens.refresh
    }
  },
  actions: {
  },
  modules: {
  }
})
