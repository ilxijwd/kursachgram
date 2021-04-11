<template>
  <v-row class="fill-height" align-content="center" justify="center">
    <v-col class="subtitle-1 text-center" cols="12"> Logging you out </v-col>
    <v-col cols="6">
      <v-progress-linear
        color="blue"
        indeterminate
        rounded
        height="6"
      ></v-progress-linear>
    </v-col>
  </v-row>
</template>

<script>
export default {
  async mounted() {
    const token = this.$store.state.app.me.token
    if (!token) return this.$router.push('/login')
    else {
      await this.$store.dispatch('$nuxtSocket/emit', {
        label: 'main',
        evt: 'logout',
      })
      this.$store.commit('app/LOGGED_OUT')
      this.$router.push('/login')
    }
  },
}
</script>
