<template>
  <v-dialog v-model="HAS_ERROR" persistent max-width="290">
    <v-card>
      <v-card-title class="headline">
        {{ ERROR.title }}
      </v-card-title>
      <v-card-text>{{ ERROR.description }} </v-card-text>
      <v-card-actions v-if="ERROR.code === 1">
        <v-btn
          color="blue"
          text
          @click.stop="RESET_ERROR() || $router.push('/login')"
        >
          Login
        </v-btn>
        <v-spacer />
        <v-btn
          color="blue"
          text
          @click.stop="RESET_ERROR() || $router.push('/register')"
        >
          Register
        </v-btn>
      </v-card-actions>
      <v-card-actions v-else-if="ERROR.code === 2">
        <v-spacer />
        <v-btn
          color="blue"
          text
          @click.stop="RESET_ERROR() || $router.push('/logout')"
        >
          Logout
        </v-btn>
      </v-card-actions>
      <v-card-actions v-else>
        <v-spacer />
        <v-btn color="blue" text @click.stop="RESET_ERROR() || $router.go()">
          Retry
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  computed: {
    ...mapGetters('socket', ['HAS_ERROR', 'ERROR']),
  },
  methods: {
    ...mapMutations('socket', ['RESET_ERROR']),
  },
}
</script>
