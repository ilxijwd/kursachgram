<template>
  <v-app dark>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item two-line>
          <v-list-item-avatar>
            <img :src="account_data.avatar_base64" />
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>
              {{ account_data.username }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ account_data.email }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav dense>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Create group</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Contacts</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-phone</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Calls</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Files</v-list-item-title>
        </v-list-item>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-cog</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Settings</v-list-item-title>
        </v-list-item>
        <v-list-item link @click.stop="$router.push('/logout')">
          <v-list-item-icon>
            <v-icon>mdi-logout</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app fixed>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
      <v-tabs color="white" centered>
        <v-tabs-slider color="white" />
        <v-tab @click.stop="$router.push('/chats')">
          <v-badge dot :value="messages">Chats</v-badge>
        </v-tab>
        <v-tab @click.stop="$router.push('/calls')">
          <v-badge dot :value="calls">Calls</v-badge>
        </v-tab>
      </v-tabs>
      <v-btn icon @click.stop="search = !search">
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <transition name="slide-right">
          <nuxt />
        </transition>
      </v-container>
    </v-main>
    <socket-error-dialog />
    <v-dialog v-model="search" max-width="290">
      <v-card>
        <v-card-title class="headline"> Search </v-card-title>
        <v-card-text>
          <v-text-field clearable />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="blue" text @click.stop="search = !search">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-footer app fixed class="flex justify-center">
      <transition name="appear">
        <v-btn
          v-if="$store.state.chats.listIsSelective"
          absolute
          top
          right
          fab
          color="red"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </transition>
      <!-- <v-speed-dial
        v-else
        v-model="fab"
        absolute
        bottom
        right
        open-on-hover
        transition="slide-y-reverse-transition"
      >
        <template #activator>
          <v-btn v-model="fab" color="blue darken-2" dark fab>
            <v-icon v-if="fab">mdi-close</v-icon>
            <v-icon v-else>mdi-plus</v-icon>
          </v-btn>
        </template>
        <v-btn fab dark small color="red">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
        <v-btn fab dark small color="indigo">
          <v-icon>mdi-account-group</v-icon>
        </v-btn>
      </v-speed-dial> -->
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapState } from 'vuex'
export default {
  data() {
    return {
      drawer: false,
      messages: 1,
      calls: 0,
      fab: false,
      search: false,
    }
  },
  computed: {
    ...mapState('auth', ['account_data']),
  },
  mounted() {
    this.socket = this.$nuxtSocket({
      auth: {
        token: this.$store.state.auth.token,
      },
    })
  },
}
</script>
