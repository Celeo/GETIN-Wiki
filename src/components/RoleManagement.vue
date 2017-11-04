<template lang="pug">
  section.section
    div.container
      h1.title Role management
      hr
      div(v-if="error")
        server-error
      nav.level(v-if="!error")
        div.level-left
          div.level-item
            b-field(label="Select a user")
              b-select(placeholder="User" v-model="selectedId")
                option(
                  v-for="user in users"
                  v-bind:value="user.id"
                  v-bind:key="user.id"
                ) {{ user.name }}
        div.level-center
          div.level-item(v-if="selectedId")
            p
              strong {{ selectedUser.name }}
              |  is
              span(v-if="selectedUser.editor")  an editor
              span(v-if="selectedUser.editor && selectedUser.admin")  and
              span(v-if="selectedUser.admin")  an admin
              span(v-if="!selectedUser.editor && !selectedUser.admin")  neither an editor nor an admin
        div.level-right(v-if="selectedId")
          div.level-item
            div.block
              button.button.is-success(
                v-bind:disabled="selectedId === 0 || selectedUser.editor"
                @click="makeEditor"
              )
                b-icon(icon="level-up")
                span Make editor
              button.button.is-success(
                v-bind:disabled="selectedId === 0 || selectedUser.admin"
                @click="makeAdmin"
              )
                b-icon(icon="level-up")
                span Make admin
              button.button.is-danger(
                v-bind:disabled="selectedId === 0 || !selectedUser.editor"
                @click="removeEditor"
              )
                b-icon(icon="level-down")
                span Revoke editor
              button.button.is-danger(
                v-bind:disabled="selectedId === 0 || !selectedUser.admin"
                @click="remokeAdmin"
              )
                b-icon(icon="level-down")
                span Revoke admin
</template>

<script>
import Vue from 'vue'
import ServerError from '../components/ServerError'


export default {
  components: {
    ServerError
  },
  data() {
    return {
      selectedId: 0,
      users: [],
      error: false
    }
  },
  computed: {
    selectedUser() {
      return this.users.filter(e => e.id === this.selectedId)[0]
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await this.$store.getters.axios(`${Vue.config.SERVER_URL}admin`)
        this.users = response.data
        this.error = false
      } catch (error) {
        this.error = true
        console.error(error)
      }
    },
    async makeChange(changeAction) {
      const toOrFrom = changeAction.direction === 'promote' ? 'to' : 'from'
      this.$dialog.confirm({
        title: 'Confirm role change',
        message: `Are you sure that you want to ${changeAction.direction}
          <strong>${this.selectedUser.name}</strong> ${toOrFrom} the ${changeAction.role} role`,
        confirmText: 'Confirm',
        type: 'is-warning',
        hasIcon: true,
        onConfirm: async () => {
          try {
            await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}admin`, {
              action: changeAction.direction,
              role: changeAction.role,
              id: this.selectedUser.id
            })
            await this.loadData()
            this.$toast.open({
              message: 'Role change successful',
              type: 'is-success'
            })
          } catch (error) {
            this.$dialog.alert({
              message: 'There was an error saving the data',
              type: 'is-danger',
              hasIcon: true
            })
          }
        }
      })
    },
    async makeEditor() {
      await this.makeChange({
        direction: 'promote',
        role: 'editor'
      })
    },
    async removeEditor() {
      await this.makeChange({
        direction: 'demote',
        role: 'editor'
      })
    },
    async makeAdmin() {
      await this.makeChange({
        direction: 'promote',
        role: 'admin'
      })
    },
    async remokeAdmin() {
      await this.makeChange({
        direction: 'demote',
        role: 'admin'
      })
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>
