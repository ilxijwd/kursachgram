<template>
  <v-app dark>
    <v-navigation-drawer v-model="drawer" app>
      <v-list class="py-0">
        <v-list-item>
          <v-list-item-content>
            <v-list-item-title class="text-h4"> Kursachgram </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider />

        <v-list-item two-line>
          <v-list-item-avatar>
            <img :src="me.avatar_base64" />
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>
              {{ me.username }}
            </v-list-item-title>
            <v-list-item-subtitle>
              {{ me.email }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <dialogs-template dialog-name="online-users">
        <template #content>
          <dialogs-sidebar-online-users />
        </template>
      </dialogs-template>

      <dialogs-template dialog-name="create-group">
        <template #content>
          <dialogs-sidebar-create-group />
        </template>
      </dialogs-template>

      <dialogs-template dialog-name="files">
        <template #content>
          <dialogs-sidebar-files />
        </template>
      </dialogs-template>

      <v-list nav dense>
        <v-list-item
          link
          @click.stop="drawer = !drawer || OPEN_DIALOG('online-users')"
        >
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Online users</v-list-item-title>
        </v-list-item>
        <v-list-item
          link
          @click.stop="drawer = !drawer || OPEN_DIALOG('create-group')"
        >
          <v-list-item-icon>
            <v-icon>mdi-account-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Create group</v-list-item-title>
        </v-list-item>
        <v-list-item
          link
          @click.stop="drawer = !drawer || OPEN_DIALOG('files')"
        >
          <v-list-item-icon>
            <v-icon>mdi-folder</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Files</v-list-item-title>
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
          <v-badge dot :value="UNREAD_MESSAGES_COUNT">Chats</v-badge>
        </v-tab>
        <v-tab @click.stop="$router.push('/users')"> Users </v-tab>
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
        <v-btn v-if="listIsSelective" absolute top right fab color="red">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </transition>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'
export default {
  data() {
    return { drawer: false, fab: false, search: false }
  },
  computed: {
    ...mapState('app', ['me', 'listIsSelective']),
    ...mapGetters('app', ['UNREAD_MESSAGES_COUNT']),
  },
  mounted() {
    this.socket = this.$nuxtSocket({
      auth: {
        token: this.$store.state.app.me.token,
      },
      name: 'main',
      persist: true,
    })
  },
  methods: {
    ...mapMutations('dialog', ['OPEN_DIALOG']),
  },
}
</script>
