<template>
  <v-app dark>
    <v-app-bar app fixed>
      <v-app-bar-title>Kursachgram</v-app-bar-title>
      <v-spacer />
      <v-avatar v-if="$store.getters['auth/AVATAR_LOADED']">
        <img :src="$store.state.auth.account_data.avatar_base64" alt="" />
      </v-avatar>
    </v-app-bar>
    <v-main>
      <v-container>
        <transition name="slide-right">
          <nuxt />
        </transition>
      </v-container>
    </v-main>
    <v-dialog v-model="showRequestErrorDialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Request error</v-card-title>
        <v-card-text>{{ $store.state.auth.request_error }}</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="blue"
            text
            @click.stop="$store.commit('auth/SET_REQUEST_ERROR', '')"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <socket-error-dialog />
    <v-footer app fixed class="flex justify-center">
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  computed: {
    showRequestErrorDialog: {
      get() {
        return !!this.$store.state.auth.request_error
      },
    },
  },
}
</script>
