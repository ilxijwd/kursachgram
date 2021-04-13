<template>
  <v-card>
    <v-card-title class="headline"> Online users </v-card-title>
    <template v-if="ONLINE_USERS.length === 0">
      <v-card-subtitle>Nobody's online 😔</v-card-subtitle>
    </template>
    <template v-else>
      <v-card-subtitle> Select someone who's online: </v-card-subtitle>
      <v-card-text>
        <v-list subheader>
          <v-subheader class="px-0">
            {{ ONLINE_USERS.length }}
            {{ ONLINE_USERS.length === 1 ? 'user' : 'users' }} online
          </v-subheader>
          <transition-group name="slide-right">
            <v-list-item
              v-for="user in ONLINE_USERS"
              :key="`user-${user.id}`"
              class="px-0"
              @click.stop="createChat(user.id)"
            >
              <v-list-item-avatar>
                <img :src="user.avatar_base64" alt="" />
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title v-text="user.username" />
              </v-list-item-content>
            </v-list-item>
          </transition-group>
        </v-list>
      </v-card-text>
    </template>
    <v-card-actions>
      <v-spacer />
      <v-btn color="blue" text @click.stop="CLOSE_DIALOG('online-users')">
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  computed: {
    ...mapGetters('app', ['ONLINE_USERS']),
  },
  mounted() {
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'app/CHAT_CREATED') {
        this.CLOSE_DIALOG('online-users')
        this.$router.push(`/chats/${mutation.payload.id}`)
      }
    })
  },
  beforeDestroy() {
    this.unsubscribe()
  },
  methods: {
    ...mapMutations('dialog', ['CLOSE_DIALOG']),
    async createChat(userId) {
      await this.$store.dispatch('$nuxtSocket/emit', {
        label: 'main',
        evt: 'create_chat',
        msg: {
          sender_id: this.$store.state.app.me.token,
          participants_ids: [userId],
        },
      })
    },
  },
}
</script>
