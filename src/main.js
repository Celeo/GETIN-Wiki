import Vue from 'vue'
import decode from 'jwt-decode'
import Buefy from 'buefy'

import store from './data'
import router from './router'
import App from './App'


Vue.use(Buefy, {
  defaultIconPack: 'fa'
})

Vue.config.productionTip = false


function loadServerUrl() {
  let url = ''
  if (process.env.NODE_ENV === 'development') {
    url = 'http://localhost:5000/'
  } else {
    url = window.location.origin + '/api/'
  }
  Vue.config.SERVER_URL = url
  console.log(`Server url: ${url}`)
}

function loadJWT() {
  let token, tokenData
  token = window.localStorage.getItem('token')
  if (token) {
    tokenData = decode(token)
    if (typeof tokenData.name !== 'undefined') {
      console.log('Requesting new session JWT from backend using localStorage token')
      // send this token to the backend to get a new session token
      const prom = store.getters.axios.post(`${Vue.config.SERVER_URL}tokens`, { token })
        .then(response => {
          token = response.data.token
          tokenData = decode(token)
          window.sessionStorage.setItem('token', token)
          console.log('Logging in via new sessionStorage token')
          store.commit('LOG_IN', { token, tokenData })
        }).catch(err => {
          // on failure, just don't log the user in, and clear the bad token from localStorage
          console.error(err)
          window.localStorage.removeItem('token')
        })
      return prom
    } else {
      console.log('Unknown token in localStorage, removing it')
      window.localStorage.removeItem('token')
    }
  } else {
    console.log('No token in localStorage')
  }
}

function loadLoginRedirect() {
  const loginRedirect = window.localStorage.getItem('loginRedirect')
  if (loginRedirect) {
    store.commit('SET_LOGIN_REDIRECT', loginRedirect)
  }
}

function createApp() {
  new Vue({
    router,
    store,
    el: '#app',
    render: h => h(App)
  })
}

loadServerUrl()
const prom = loadJWT()
if (prom !== null && typeof prom !== 'undefined') {
  prom.then(() => {
    const loginRedirect = window.localStorage.getItem('loginRedirect')
    if (loginRedirect !== null) {
      router.push(loginRedirect)
    }
    createApp()
  })
} else {
  loadLoginRedirect()
  createApp()
}
