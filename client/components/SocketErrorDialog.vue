<template>
  <v-dialog v-model="SOCKET_HAS_ERROR" persistent max-width="290">
    <v-card>
      <v-card-title class="headline">
        {{ SOCKET_ERROR_TITLE }}
      </v-card-title>
      <v-card-text>{{ SOCKET_ERROR_DESCRIPTION }} </v-card-text>
      <v-card-actions v-if="SOCKET_ERROR_TYPE === 'no_connection'">
        <v-spacer />
        <v-btn color="blue" text @click.stop="$router.go()">Retry</v-btn>
      </v-card-actions>
      <v-card-actions v-else-if="SOCKET_ERROR_TYPE === 'invalid_token'">
        <v-spacer />
        <v-btn color="blue" text @click.stop="$router.push('/logout')">
          Logout
        </v-btn>
      </v-card-actions>
      <v-card-actions v-else-if="SOCKET_ERROR_TYPE === 'not_registered'">
        <v-spacer />
        <v-btn color="blue" text @click.stop="$router.push('/logout')">
          Logout
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters('socket', {
      SOCKET_HAS_ERROR: 'HAS_ERROR',
      SOCKET_ERROR_TYPE: 'ERROR_TYPE',
      SOCKET_ERROR_TITLE: 'ERROR_TITLE',
      SOCKET_ERROR_DESCRIPTION: 'ERROR_DESCRIPTION',
    }),
  },
}
</script>
