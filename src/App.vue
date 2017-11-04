<template lang="pug">
  div
    nav.nav.has-shadow
      div.container
        div.nav-left
          router-link#brand.nav-item(:to="'/'") Wiki
        div.nav-center.nav-menu
          div.nav-item(v-if="loggedIn")
            div.block
              button.button.is-info(@click="newPageModalActive = true")
                b-icon(icon="plus")
                span New page
        div.nav-right.nav-menu
          router-link.nav-item.is-tab(
            :to="{ name: 'Landing' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Landing' }"
          ) Home
          router-link.nav-item.is-tab(
            :to="{ name: 'Login' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Login' }"
            v-if="!loggedIn"
          ) Log in
          router-link.nav-item.is-tab(
            :to="{ name: 'Index' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Index' }"
            v-if="loggedIn"
          ) Index
          router-link.nav-item.is-tab(
            :to="{ name: 'Admin' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Admin' }"
            v-if="$store.getters.admin"
          ) Admin
          router-link.nav-item.is-tab(
            :to="{ name: 'Logout' }"
            v-bind:class="{ 'is-active': $router.currentRoute.name == 'Logout' }"
            v-if="loggedIn"
          ) Log out
    transition(name="fade" mode="out-in")
      router-view
    b-modal(
      v-bind:active.sync="newPageModalActive"
      v-bind:component="NewPageModal"
      v-bind:width="400"
    )
</template>

<script>
import NewPageModal from './components/NewPageModal'


export default {
  data() {
    return {
      NewPageModal,
      newPageModalActive: false
    }
  },
  computed: {
    loggedIn() {
      return this.$store.getters.isLoggedIn
    },
    member() {
      return this.$store.getters.inAlliance
    }
  }
}
</script>

<!-- Buefy customization -->
<style lang="scss">
@import "~bulma/sass/utilities/_all";

$primary: $blue;
$primary-invert: findColorInvert($primary);

$colors: (
    "white": ($white, $black),
    "black": ($black, $white),
    "light": ($light, $light-invert),
    "dark": ($dark, $dark-invert),
    "primary": ($primary, $primary-invert),
    "info": ($info, $info-invert),
    "success": ($success, $success-invert),
    "warning": ($warning, $warning-invert),
    "danger": ($danger, $danger-invert)
);

$link: $primary;
$link-invert: $primary-invert;
$link-focus-border: $primary;

.button {
  margin-left: 5px;
}

@import "~bulma";
@import "~buefy/src/scss/buefy";
</style>

<!-- App css -->
<style lang="stylus">
#brand
  font-weight 600
  font-size 24px

label.label
  font-weight 600 !important

.fade-enter-active, .fade-leave-active
  transition opacity .2s

.fade-enter, .fade-leave-active
  opacity 0
</style>
