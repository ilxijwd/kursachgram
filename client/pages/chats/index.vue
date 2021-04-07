<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <template v-if="chats.length === 0">
        <v-card>
          <v-card-title>No chats available</v-card-title>
          <v-card-subtitle>Select someone who's online:</v-card-subtitle>
        </v-card>
        <v-list class="mt-3">
          <v-subheader>
            {{ ONLINE_USERS.length }}
            {{ ONLINE_USERS.length === 1 ? 'user' : 'users' }} online
          </v-subheader>
          <v-list-item-group>
            <template v-for="(user, index) in ONLINE_USERS">
              <v-list-item
                :key="`user-${user.id}`"
                @click.stop="$router.push(`/chats/`)"
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
      </template>
      <v-list v-else two-line>
        <v-list-item-group
          v-model="selectedChats"
          multiple
          active-class="blue--text"
        >
          <template v-for="(chat, index) in chats">
            <v-list-item
              :key="chat.title"
              @mousedown.stop="mouseDown(index, chat.id)"
              @mouseup.stop="mouseUp(chat.id)"
            >
              <template #default="{ active }">
                <v-list-item-avatar color="blue">
                  <transition name="flip" mode="out-in">
                    <v-icon v-if="listIsSelective && active" color="white">
                      mdi-check
                    </v-icon>
                    <img v-else src="" alt="" />
                  </transition>
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title v-text="chat.title">
                    <v-icon></v-icon>
                  </v-list-item-title>
                  <v-list-item-subtitle
                    class="text--primary"
                    v-text="chat.lastToText"
                  />
                  <v-list-item-subtitle v-text="chat.subtitle" />
                </v-list-item-content>
                <v-list-item-action>
                  <v-list-item-action-text v-text="chat.action" />
                  <v-badge
                    overlap
                    :value="chat.unreadMessages"
                    :content="chat.unreadMessages"
                  >
                    <v-icon
                      v-if="chat.type === 'personal'"
                      color="grey lighten-1"
                    >
                      mdi-account
                    </v-icon>
                    <v-icon v-else color="grey lighten-1">
                      mdi-account-multiple
                    </v-icon>
                  </v-badge>
                </v-list-item-action>
              </template>
            </v-list-item>
            <v-divider v-if="index < chats.length - 1" :key="index" />
          </template>
        </v-list-item-group>
      </v-list>
    </v-col>
  </v-row>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'

export default {
  middleware: ['authenticated'],
  data() {
    return {
      holdTimeMs: 250,
      mouseDownActive: false,
      selectedChats: [],
    }
  },
  computed: {
    ...mapState('chats', ['listIsSelective', 'chats', 'onlineUsers']),
    ...mapGetters('chats', ['ONLINE_USERS']),
  },
  watch: {
    selectedChats(newItem) {
      if (newItem.length === 0) this.SET_LIST_IS_SELECTIVE(false)
    },
  },
  methods: {
    ...mapMutations('chats', ['SET_LIST_IS_SELECTIVE']),
    mouseDown(itemIndex) {
      this.mouseDownActive = true
      setTimeout(() => {
        if (this.mouseDownActive)
          if (!this.listIsSelective && this.selectedChats.length === 0) {
            this.selectedChats.push(itemIndex)
            this.selectedChats.push(itemIndex)
            this.SET_LIST_IS_SELECTIVE(true)
          }
      }, this.holdTimeMs)
    },
    mouseUp(chatId) {
      this.mouseDownActive = false
      if (!this.listIsSelective)
        setTimeout(() => this.$router.push(`/chats/${chatId}`), this.holdTimeMs)
    },
  },
}
</script>
