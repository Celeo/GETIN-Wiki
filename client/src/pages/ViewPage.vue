<template lang="pug">
  section.section
    div.container
      div(v-if="error")
        article.message.is-warning
          div.message-header
            p
              strong This page does not exist
          div.message-body
            p If you want to create it, do so using the <strong>Add new page</strong> button above
      div(v-if="!error && page")
        nav.level
          div.level-left
            div.level-item
            h1.title {{ page.name }}
          div.level-right
            div.level-item
              button.button(@click="edit")
                b-icon(icon="pencil")
                span Edit
        div.content(v-html="markdown")
</template>

<script>
import Vue from 'vue'
import marked from 'marked'
import { renderer } from '../util'


export default {
  data() {
    return {
      error: false,
      page: null
    }
  },
  computed: {
    markdown() {
      if (this.page.content) {
        return marked(this.page.content, { sanitize: true, renderer })
      } else {
        return 'No data in this page'
      }
    }
  },
  async created() {
    try {
      const response = await this.$store.getters.axios.get(
        `${Vue.config.SERVER_URL}lookup/${this.$route.params.category}/${this.$route.params.page}`
      )
      this.page = response.data
      this.error = false
    } catch (error) {
      console.error(error)
      this.error = true
    }
  },
  methods: {
    async edit() {
      // TODO
    }
  }
}
</script>
