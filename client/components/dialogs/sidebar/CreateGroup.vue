<template>
  <v-card>
    <v-card-title class="headline"> Online users </v-card-title>
    <template v-if="ONLINE_USERS.length === 0">
      <v-card-subtitle>Nobody's online 😔</v-card-subtitle>
    </template>
    <template v-else>
      <v-card-subtitle> Select someone who's online: </v-card-subtitle>
      <v-card-text>
        <v-file-input
          v-if="selectedChats.length >= 2"
          ref="avatarInput"
          v-model="avatar"
          :rules="avatarRules"
          prepend-icon=""
          truncate-length="15"
          show-size
          accept="image/png, image/jpeg, image/jpg"
          placeholder="Pick an avatar"
          label="Avatar"
          @change="fileOnChangeEvent"
        />
        <v-text-field
          v-if="selectedChats.length >= 2"
          v-model="groupName"
          label="Group name"
        />
        <v-list subheader>
          <v-subheader class="px-0">
            {{ ONLINE_USERS.length }}
            {{ ONLINE_USERS.length === 1 ? 'user' : 'users' }} online
          </v-subheader>
          <v-list-item-group v-model="selectedChats" multiple>
            <v-list-item
              v-for="user in ONLINE_USERS"
              :key="`user-${user.id}`"
              class="px-0"
            >
              <template #default="{ active }">
                <v-list-item-avatar>
                  <img :src="user.avatar_base64" alt="" />
                </v-list-item-avatar>
                <v-list-item-content>
                  <v-list-item-title>
                    {{ user.username }}
                  </v-list-item-title>
                </v-list-item-content>
                <v-list-item-action>
                  <v-checkbox :input-value="active" color="blue" />
                </v-list-item-action>
              </template>
            </v-list-item>
          </v-list-item-group>
        </v-list>
      </v-card-text>
    </template>
    <v-card-actions>
      <v-spacer />
      <v-btn
        color="blue"
        text
        :disabled="selectedChats.length < 2 || groupName === '' || !avatar"
        @click.stop="createChat"
      >
        Create group
      </v-btn>
      <v-btn color="blue" text @click.stop="CLOSE_DIALOG('create-group')">
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  data() {
    return {
      groupName: '',
      selectedChats: [],
      avatar: null,
      avatarBase64: '',
      avatarRules: [
        (v) => !!v || 'Avatar is required',
        (v) => v?.size < 1000000 || 'Avatar size should be less than 1 MB',
      ],
    }
  },
  computed: {
    ...mapGetters('app', ['ONLINE_USERS']),
  },
  mounted() {
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'app/CHAT_CREATED') {
        this.CLOSE_DIALOG('create-group')
        this.$router.push(`/chats/${mutation.payload.id}`)
      }
    })
  },
  beforeDestroy() {
    this.unsubscribe()
  },
  methods: {
    ...mapMutations('dialog', ['CLOSE_DIALOG']),
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
      })
    },
    async fileOnChangeEvent() {
      this.avatarBase64 = this.avatar
        ? await this.fileToBase64(this.avatar)
        : ''
    },
    async createChat() {
      const users = this.ONLINE_USERS.filter((_, i) =>
        this.selectedChats.includes(i)
      )

      if (users.length > 2 && this.groupName !== '')
        await this.$store.dispatch('$nuxtSocket/emit', {
          label: 'main',
          evt: 'create_chat',
          msg: {
            sender_id: this.$store.state.app.me.token,
            participants_ids: users.map((u) => u.id),
            name: this.groupName,
            avatar_base64: this.avatarBase64,
          },
        })
    },
  },
}
</script>
