<template>
  <v-card>
    <v-card-title class="headline"> Online users </v-card-title>
    <template v-if="ONLINE_USERS.length === 0">
      <v-card-subtitle>Nobody's online 😔</v-card-subtitle>
    </template>
    <template v-else>
      <v-card-subtitle> Select someone who's online: </v-card-subtitle>
      <v-card-text>
        <v-list class="mt-3">
          <v-subheader>
            {{ ONLINE_USERS.length }}
            {{ ONLINE_USERS.length === 1 ? 'user' : 'users' }} online
          </v-subheader>
          <v-list-item-group>
            <template v-for="(user, index) in ONLINE_USERS">
              <v-list-item
                :key="`user-${user.id}`"
                @click.stop="createChat(user.id)"
              >
                <v-list-item-avatar>
                  <img :src="user.avatar_base64" alt="" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title v-text="user.username" />
                </v-list-item-content>
              </v-list-item>
              <v-divider v-if="index < ONLINE_USERS.length - 1" :key="index" />
            </template>
          </v-list-item-group>
        </v-list>
      </v-card-text>
    </template>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  computed: {
    ...mapGetters('chats', ['ONLINE_USERS']),
  },
}
</script>
