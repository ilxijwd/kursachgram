<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <template v-if="chats.length !== 0">
        <v-card>
          <v-card-title v-if="UNREAD_MESSAGES_COUNT > 0">
            You have {{ UNREAD_MESSAGES_COUNT }} unread message{{
              UNREAD_MESSAGES_COUNT > 1 ? 's' : ''
            }}
          </v-card-title>
          <v-card-title v-else>Available chats</v-card-title>
        </v-card>
        <v-card class="mt-3">
          <v-card-text class="px-0">
            <v-list two-line class="py-0">
              <v-list-item-group
                v-model="selectedChats"
                multiple
                active-class="blue--text"
              >
                <v-list-item
                  v-for="(chat, index) in chats"
                  :key="chat.id"
                  @mousedown.stop="mouseDown(index, chat.id)"
                  @mouseup.stop="mouseUp(chat.id)"
                >
                  <template #default="{ active }">
                    <v-list-item-avatar color="blue">
                      <transition name="flip" mode="out-in">
                        <v-icon v-if="listIsSelective && active" color="white">
                          mdi-check
                        </v-icon>
                        <img v-else :src="chat.avatar_base64" alt="" />
                      </transition>
                    </v-list-item-avatar>

                    <v-list-item-content>
                      <v-list-item-title>
                        <v-icon v-if="chat.participants.length > 2">
                          mdi-account-multiple
                        </v-icon>
                        {{ chat.name }}
                      </v-list-item-title>
                      <v-list-item-subtitle class="text--primary">
                        {{ GET_LATEST_MESSAGE(chat) }}
                      </v-list-item-subtitle>
                    </v-list-item-content>

                    <v-list-item-action>
                      <v-list-item-action-text>
                        {{ $moment(GET_LATEST_ACTION_TIME(chat)).from(now) }}
                      </v-list-item-action-text>
                      <v-list-item-action-text>
                        <v-chip
                          v-if="GET_UNREAD_MESSAGES_COUNT(chat) > 0"
                          x-small
                        >
                          {{ GET_UNREAD_MESSAGES_COUNT(chat) }}
                        </v-chip>
                      </v-list-item-action-text>
                    </v-list-item-action>
                  </template>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card-text>
        </v-card>
      </template>
      <template v-else>
        <v-card>
          <v-card-title>No messages 😢</v-card-title>
          <v-card-subtitle>
            Select somebody who's online or create a group
          </v-card-subtitle>
        </v-card>
      </template>
    </v-col>
  </v-row>
</template>

<script>
import { mapState, mapGetters, mapMutations } from 'vuex'

export default {
  middleware: ['authenticated'],
  data() {
    return {
      now: Date.now(),
      holdTimeMs: 250,
      mouseDownActive: false,
      selectedChats: [],
    }
  },
  computed: {
    ...mapState('app', ['listIsSelective', 'chats', 'onlineUsers']),
    ...mapGetters('app', [
      'ONLINE_USERS',
      'UNREAD_MESSAGES_COUNT',
      'GET_LATEST_MESSAGE',
      'GET_LATEST_ACTION_TIME',
      'GET_UNREAD_MESSAGES_COUNT',
    ]),
  },
  watch: {
    selectedChats(newItem) {
      if (newItem.length === 0) this.SET_LIST_IS_SELECTIVE(false)
    },
  },
  beforeMount() {
    this.interval = setInterval(() => (this.now = Date.now()), 1000)
  },
  destroyed() {
    clearInterval(this.interval)
  },
  methods: {
    ...mapMutations('app', ['SET_LIST_IS_SELECTIVE']),
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
    async createChat(participantsId) {
      await this.$store.dispatch('$nuxtSocket/emit', {
        label: 'main',
        evt: 'create_chat',
        msg: {
          participants_ids: [participantsId],
        },
      })
      // this.$router.push(`/chats/${participantsIds}`)
    },
  },
}
</script>
