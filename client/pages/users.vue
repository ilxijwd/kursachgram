<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <template v-if="users.length !== 0">
        <v-card>
          <v-card-title v-if="ONLINE_USERS > 0">
            There are {{ ONLINE_USERS }} user{{ ONLINE_USERS > 1 ? 's' : '' }}
            online
          </v-card-title>
          <v-card-title v-else>Registered users</v-card-title>
        </v-card>
        <v-card class="mt-3">
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="user in users"
                :key="`user-${user.id}`"
                class="px-0"
                @click.stop="createChat(user.id)"
              >
                <template v-if="user.online">
                  <v-badge bottom dot overlap color="green">
                    <v-list-item-avatar class="ma-0">
                      <img :src="user.avatar_base64" alt="" />
                    </v-list-item-avatar>
                  </v-badge>
                  <v-list-item-content class="ml-4">
                    <v-list-item-title v-text="user.username" />
                  </v-list-item-content>
                </template>
                <template v-else>
                  <v-list-item-avatar>
                    <img :src="user.avatar_base64" alt="" />
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title v-text="user.username" />
                    <v-list-item-subtitle
                      v-text="
                        `Last seen ${$moment
                          .unix(user.logout_timestamp)
                          .from(now)}`
                      "
                    />
                  </v-list-item-content>
                </template>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </template>
      <template v-else>
        <v-card>
          <v-card-title>No users 😢</v-card-title>
          <v-card-subtitle>
            Tell somebody to register, please...
          </v-card-subtitle>
        </v-card>
      </template>
    </v-col>
  </v-row>
</template>

<script>
import { mapState, mapGetters } from 'vuex'
export default {
  middleware: ['authenticated'],
  data() {
    return {
      now: Date.now(),
    }
  },
  computed: {
    ...mapState('app', ['users']),
    ...mapGetters('app', ['ONLINE_USERS']),
  },
  beforeMount() {
    this.interval = setInterval(() => (this.now = Date.now()), 1000)
  },
  mounted() {
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'app/CHAT_CREATED') {
        this.$router.push(`/chats/${mutation.payload.id}`)
      }
    })
  },
  beforeDestroy() {
    this.unsubscribe()
  },
  destroyed() {
    clearInterval(this.interval)
  },
  methods: {
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
