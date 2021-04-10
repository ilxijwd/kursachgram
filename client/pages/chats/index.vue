<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <template v-if="PRIVATE_MESSAGES.length !== 0">
        <v-card>
          <v-card-title>Direct messages</v-card-title>
        </v-card>
        <v-list two-line class="mt-3">
          <v-list-item-group
            v-model="selectedChats"
            multiple
            active-class="blue--text"
          >
            <template v-for="(message, index) in PRIVATE_MESSAGES">
              <v-list-item
                :key="message.recieved_at"
                @mousedown.stop="mouseDown(index, message.chat.id)"
                @mouseup.stop="mouseUp(message.chat.id)"
              >
                <template #default="{ active }">
                  <v-list-item-avatar color="blue">
                    <transition name="flip" mode="out-in">
                      <v-icon v-if="listIsSelective && active" color="white">
                        mdi-check
                      </v-icon>
                      <img
                        v-else
                        :src="
                          CHAT_AVATAR(
                            message.chat.id,
                            $store.state.auth.user.id
                          )
                        "
                        alt=""
                      />
                    </transition>
                  </v-list-item-avatar>
                  <v-list-item-content>
                    <v-list-item-title>
                      {{
                        message.chat.participants_ids.find(
                          (p) => p !== $store.state.auth.user.id
                        ).username
                      }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="text--primary">
                      {{
                        message.sender_id === $store.state.auth.user.id
                          ? 'You'
                          : $store.state.chats.users.find(
                              (u) => u.id === message.sender_id
                            ).username
                      }}:
                      <template v-if="message.files.length > 1">
                        <v-icon> mdi-file-document-multiple </v-icon>
                        {{ message.files.length }} files
                      </template>
                      <template v-else-if="message.files.length === 1">
                        <v-icon> mdi-file-document </v-icon>
                        {{ message.files.length }} file
                      </template>
                      <template v-else>
                        {{ message.content }}
                      </template>
                    </v-list-item-subtitle>
                  </v-list-item-content>
                  <v-list-item-action>
                    <v-list-item-action-text v-text="message.recieved_at" />
                    <v-chip v-if="message.chat.unread_messages_count > 0">
                      {{ message.chat.unread_messages_count }}
                    </v-chip>
                  </v-list-item-action>
                </template>
              </v-list-item>
              <v-divider v-if="index < chats.length - 1" :key="index" />
            </template>
          </v-list-item-group>
        </v-list>
      </template>
      <template v-if="GROUP_MESSAGES.length !== 0">
        <v-card class="mt-3">
          <v-card-title>Group messages</v-card-title>
        </v-card>
        <v-list two-line class="mt-3"> </v-list>
      </template>
      <template
        v-if="PRIVATE_MESSAGES.length === 0 && GROUP_MESSAGES.length === 0"
      >
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
      holdTimeMs: 250,
      mouseDownActive: false,
      selectedChats: [],
    }
  },
  computed: {
    ...mapState('chats', ['listIsSelective', 'chats', 'onlineUsers']),
    ...mapGetters('chats', [
      'ONLINE_USERS',
      'CHAT_AVATAR',
      'PRIVATE_MESSAGES',
      'GROUP_MESSAGES',
    ]),
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
