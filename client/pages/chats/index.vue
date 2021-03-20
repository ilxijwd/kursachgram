<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="8" md="6">
      <v-list two-line>
        <v-list-item-group
          v-model="selected"
          :multiple="selective"
          active-class="blue--text"
        >
          <template v-for="(chat, index) in chats">
            <v-list-item
              :key="chat.title"
              @mousedown.stop="mouseDown(chat.id)"
              @mouseup.stop="mouseUp"
            >
              <v-list-item-content>
                <v-list-item-title v-text="chat.title" />

                <v-list-item-subtitle
                  class="text--primary"
                  v-text="chat.lastToText"
                />

                <v-list-item-subtitle v-text="chat.subtitle" />
              </v-list-item-content>

              <v-list-item-action>
                <template v-if="!selective">
                  <v-list-item-action-text v-text="chat.action" />

                  <v-badge
                    overlap
                    :value="chat.unreadMessages"
                    :content="chat.unreadMessages"
                  >
                    <v-icon color="grey lighten-1">
                      {{
                        chat.type === 'personal'
                          ? 'mdi-account'
                          : 'mdi-account-group'
                      }}
                    </v-icon>
                  </v-badge>
                </template>
                <template v-else>
                  <v-checkbox :input-value="chat.selected"></v-checkbox>
                </template>
              </v-list-item-action>
            </v-list-item>

            <v-divider v-if="index < chats.length - 1" :key="index" />
          </template>
        </v-list-item-group>
      </v-list>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      heldStart: 0,
      heldId: -1,
      selected: -1,
      selective: false,
      chats: [
        {
          id: 1,
          title: 'Iluxan',
          lastToText: '⠀',
          unreadMessages: 2,
          subtitle: `I'll be in your neighborhood doing errands this weekend. Do you want to hang out?`,
          action: '15 min',
          type: 'personal',
          selected: false,
        },
        {
          id: 2,
          title: 'You, Iluxan',
          lastToText: 'You',
          unreadMessages: 4,
          action: '2 hr',
          subtitle: `Wish I could come, but I'm out of town this weekend.`,
          type: 'group',
          selected: false,
        },
        {
          id: 3,
          title: 'You, Iluxan',
          lastToText: 'Iluxan',
          action: '6 hr',
          unreadMessages: 0,
          subtitle: 'Do you have Paris recommendations? Have you ever been?',
          type: 'personal',
          selected: false,
        },
      ],
    }
  },
  methods: {
    mouseDown(chatId) {
      this.heldId = chatId
      this.heldStart = Date.now()
    },
    mouseUp() {
      if (Date.now() - this.heldStart > 500) this.selective = !this.selective
      else if (!this.selective)
        setTimeout(() => this.$router.push(`/chats/${this.heldId}`), 250)
    },
  },
}
</script>
