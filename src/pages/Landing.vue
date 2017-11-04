<template lang="pug">
  div
    section.section.span
      div.container
        div.heading
          h1.title Wiki for GETIN
        br
        p
          | This app functions like to a wiki to share knowledge amongst alliance members.
          br
          |  To view the articles, click the <strong>Log in</strong> link in the top right to sign in
          |  with EVE's
          strong  SSO
          |  and then a
          strong  Index
          |  button will appear.
    section.section.footer
      div.container
        div.content.has-text-centered
          p
            strong GETIN-Wiki
            |  by
            strong  Celeo
          p
            a.icon(href="https://github.com/Celeo/GETIN-Wiki" target="_blank")
              i.fa.fa-github
</template>

<script>
export default {
  async created() {
    this.$store.commit('CLEAR_LOGIN_REDIRECT')
  }
}
</script>

<style lang="stylus" scoped>
section.span
  height 80vh
</style>
