<template>
  <v-app dark>
    <v-app-bar app fixed>
      <v-app-bar-title>Kursachgram</v-app-bar-title>
    </v-app-bar>
    <v-main>
      <v-container>
        <transition name="slide-right">
          <nuxt />
        </transition>
      </v-container>
    </v-main>
    <socket-error-dialog />
    <v-footer app fixed class="flex justify-center">
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  mounted() {
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'app/LOGGED_IN') {
        this.$store.commit('socket/SET_LOADING', false)
        this.$router.push('/chats')
      }
    })

    this.socket = this.$nuxtSocket({
      name: 'main',
      persist: true,
    })
  },
  beforeDestroy() {
    this.unsubscribe()
  },
}
</script>
