import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'


Vue.use(Vuex)

const state = {
  token: null,
  name: null,
  inAlliance: false,
  editor: false,
  admin: false,
  axios: axios.create(),
  postLoginDestination: null
}

const mutations = {
  LOG_IN(state, payload) {
    const { token, tokenData } = payload
    state.token = token
    state.name = tokenData.name
    state.inAlliance = tokenData.inAlliance
    state.editor = tokenData.editor
    state.admin = tokenData.admin
    state.axios = axios.create({ headers: { Authorization: token } })
  },

  LOG_OUT(state) {
    state.token = null
    state.name = null
    state.inAlliance = false
    state.editor = false
    state.admin = false
    state.axios = axios.create()
  },

  SET_LOGIN_REDIRECT(state, payload) {
    state.postLoginDestination = payload
    window.localStorage.setItem('loginRedirect', payload)
  },

  CLEAR_LOGIN_REDIRECT(state) {
    state.postLoginDestination = null
    window.localStorage.clearItem('loginRedirect')
  }
}

const getters = {
  token(state) {
    return state.token
  },

  name(state) {
    return state.name
  },

  isLoggedIn(state) {
    return !!state.name
  },

  inAlliance(state) {
    return state.inAlliance
  },

  editor(state) {
    return state.editor
  },

  admin(state) {
    return state.admin
  },

  axios(state) {
    return state.axios
  },

  postLoginDestination(state) {
    return state.postLoginDestination
  }
}


export default new Vuex.Store({
  state,
  mutations,
  getters
})
