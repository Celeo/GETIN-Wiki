<template lang="pug">
  section.section
    div.container
      div(v-if="error")
        server-error
      div.content(v-if="!error && originalPage")
        nav.level
          div.level-left
            div.level-item
              b-field(label="Name")
                b-input(:value="originalPage.name" v-model="newTitle")
            div.level-item
              b-field(label="Category")
                b-select(placeholder="category" v-model="newCategoryId")
                  option(
                    v-for="category in categories"
                    v-bind:value="category.id"
                    v-bind:key="category.id"
                  ) {{ category.name }}
          div.level-right
            div.level-item
              div.block
                router-link.button(:to="pageUrlData" v-if="!dirty")
                  b-icon(icon="arrow-left")
                  span Back to page
                button.button.is-warning(v-if="dirty" @click="checkAbandon")
                  b-icon(icon="ban")
                  span Abandon changes
                button.button.is-success(@click="save" v-bind:disabled="!dirty")
                  b-icon(icon="floppy-o")
                  span Save changes
        hr
        div.columns
          div#panel-input.column.is-half
            p.control
              textarea#entry.textarea(v-model="newContent")
          div.column.is-half
            div#panel-output(v-html="renderedContent")
</template>

<script>
import Vue from 'vue'
import ServerError from '../components/ServerError'
import marked from 'marked'
import { renderer } from '../util'


export default {
  components: {
    ServerError
  },
  data() {
    return {
      error: false,
      originalPage: null,
      newTitle: '',
      newContent: '',
      newCategoryId: '',
      categories: []
    }
  },
  computed: {
    dirty() {
      return this.newContent !== this.originalPage.content || this.newTitle !== this.originalPage.name
    },
    renderedContent() {
      if (this.newContent) {
        return marked(this.newContent, { sanitize: true, renderer })
      } else {
        return ''
      }
    },
    pageUrlData() {
      return { name: 'ViewPage', params: { category: this.originalPage.category_name, page: this.originalPage.name } }
    }
  },
  methods: {
    async loadData() {
      try {
        const pageResponse = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}page/${this.$route.params.pageId}`)
        this.originalPage = pageResponse.data
        this.newTitle = this.originalPage.name
        this.newContent = this.originalPage.content
        const categoriesResponse = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}category`)
        this.categories = categoriesResponse.data
        this.newCategoryId = this.originalPage.category_id
        this.error = false
      } catch (error) {
        console.error(error)
        this.error = true
      }
    },
    async save() {
      if (!this.dirty) {
        this.$toast.open({
          message: 'No changes have been made'
        })
        return
      }
      try {
        const data = {
          name: this.newTitle,
          category_id: this.newCategoryId,
          content: this.newContent
        }
        await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}page/${this.$route.params.pageId}`, data)
        await this.loadData()
        this.$toast.open({
          message: 'Page saved',
          type: 'is-success'
        })
      } catch (error) {
        console.error(error)
        this.$dialog.alert({
          message: 'There was an error saving the data',
          type: 'is-danger',
          hasIcon: true
        })
      }
    },
    checkAbandon() {
      if (this.dirty) {
        this.$dialog.confirm({
          title: 'Confirm',
          message: 'You have unsaved changes. Are you sure you want to cancel editing?',
          type: 'is-warning',
          hasIcon: true,
          onConfirm: () => {
            this.$router.push(this.pageUrlData)
          }
        })
      } else {
        this.$router.push(this.pageUrlData)
      }
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>

<style lang="stylus" scoped>
#panel-input
  border-right 1px solid rgba(0, 0, 0, 0.3)

#panel-output
  height 65vh
  overflow-y scroll

#entry
  height 70vh !important
</style>
