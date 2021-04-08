<template>
  <v-app dark>
    <v-app-bar app fixed>
      <v-app-bar-title>Kursachgram</v-app-bar-title>
      <v-spacer />
      <v-avatar v-if="!!avatar_base64">
        <img :src="avatar_base64" alt="" />
      </v-avatar>
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
import { mapState } from 'vuex'
export default {
  computed: {
    ...mapState('auth', {
      avatar_base64: (state) => state.user.avatar_base64,
    }),
  },
  mounted() {
    this.socket = this.$nuxtSocket({
      name: 'main',
      persist: true,
    })
  },
}
</script>
