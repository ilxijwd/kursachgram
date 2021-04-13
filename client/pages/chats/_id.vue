<template>
  <div class="mt-10">
    <v-container ref="messages-box" class="pa-0">
      <v-row
        v-for="message in CHAT_BY_ID($route.params.id).messages"
        :key="`message-${message.id}`"
      >
        <template v-if="message.sender.id === $store.state.app.me.id">
          <v-col cols="2" class="pt-0 mr-1">
            <v-avatar size="56">
              <img :src="message.sender.avatar_base64" alt="" />
            </v-avatar>
          </v-col>
          <v-col class="py-0">
            <v-textarea
              :value="message.content"
              :label="`${message.sender.username} - ${$moment(
                message.received_at
              ).calendar()}`"
              readonly
              outlined
              auto-grow
              rows="1"
            />
            <v-container
              v-if="message.files.length > 0"
              class="mt-n8 mb-6 px-0"
            >
              <v-chip
                v-for="(file, index) in message.files"
                :key="`${message.id}-file-${index}`"
                class="mr-2"
                @click="downloadFile(file)"
              >
                <v-icon left>
                  {{
                    isImage(file.mime)
                      ? 'mdi-image'
                      : isVideo(file.mime)
                      ? 'mdi-video'
                      : isAudio(file.mime)
                      ? 'mdi-microphone'
                      : 'mdi-file-document'
                  }}
                </v-icon>
                {{ file.filename }}
              </v-chip>
            </v-container>
          </v-col>
        </template>
        <template v-else>
          <v-col class="py-0">
            <v-textarea
              :value="message.content"
              :label="`${message.sender.username} - ${$moment(
                message.received_at
              ).calendar()}`"
              readonly
              outlined
              auto-grow
              rows="1"
            />
            <v-container
              v-if="message.files.length > 0"
              class="mt-n8 mb-6 px-0"
            >
              <v-chip
                v-for="(file, index) in message.files"
                :key="`${message.id}-file-${index}`"
                class="mr-2"
                @click="downloadFile(file)"
              >
                <v-icon left>
                  {{
                    isImage(file.mime)
                      ? 'mdi-image'
                      : isVideo(file.mime)
                      ? 'mdi-video'
                      : isAudio(file.mime)
                      ? 'mdi-microphone'
                      : 'mdi-file-document'
                  }}
                </v-icon>
                {{ file.filename }}
              </v-chip>
            </v-container>
          </v-col>
          <v-col cols="2" class="pt-0 pl-0 mr-2">
            <v-avatar size="56">
              <img :src="message.sender.avatar_base64" alt="" />
            </v-avatar>
          </v-col>
        </template>
      </v-row>
    </v-container>
    <v-footer app>
      <v-text-field
        v-model="text"
        clearable
        filled
        label="Your message..."
        type="text"
      >
        <template #prepend>
          <v-badge
            :content="files.length"
            :value="files.length !== 0"
            overlap
            class="mr-2"
          >
            <v-btn icon @click.stop="selectFiles">
              <v-icon> mdi-paperclip </v-icon>
            </v-btn>
          </v-badge>
        </template>
        <template #append-outer>
          <v-btn icon @click.stop="sendMessage">
            <v-icon v-if="(text && text.length !== 0) || files.length !== 0">
              mdi-send
            </v-icon>
            <v-icon v-else> mdi-send-lock </v-icon>
          </v-btn>
        </template>
      </v-text-field>
    </v-footer>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  middleware: ['authenticated'],
  validate({ params, store }) {
    return !!store.state.app.chats.find((c) => c.id === params.id)
  },
  data() {
    return {
      text: '',
      files: [],
    }
  },
  computed: {
    ...mapGetters('app', ['CHAT_BY_ID']),
  },
  mounted() {
    this.$store.commit('app/MARK_SEEN', this.$route.params.id)
    this.$nextTick(() => {
      window.scrollTo(0, document.body.clientHeight)
    })
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'app/MESSAGE_SENT') {
        this.$store.commit('app/MARK_SEEN', this.$route.params.id)
        this.$nextTick(() => {
          window.scrollTo(0, document.body.scrollHeight)
        })
      }
    })
  },
  destroyed() {
    this.unsubscribe()
  },
  methods: {
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
      })
    },
    selectFiles() {
      this.files = []
      const input = document.createElement('input')
      input.type = 'file'
      input.multiple = true
      input.onchange = (e) => {
        this.files = Array.from(e.target.files)
      }
      input.click()
    },
    isImage(fileMime) {
      return [
        'image/gif',
        'image/vnd.microsoft.icon',
        'image/jpeg',
        'image/png',
        'image/bmp',
        'image/svg+xml',
        'image/webp',
      ].includes(fileMime)
    },
    isVideo(fileMime) {
      return [
        'video/x-msvideo',
        'video/mpeg',
        'video/ogg',
        'video/webm',
        'video/3gpp',
        'video/3gpp2',
      ].includes(fileMime)
    },
    isAudio(fileMime) {
      return [
        'audio/aac',
        'video/x-msvideo',
        'audio/mpeg',
        'audio/ogg',
        'audio/wav',
        'audio/3gpp',
        'audio/3gpp2',
      ].includes(fileMime)
    },
    downloadFile(file) {
      const a = document.createElement('a')
      a.href = file.base64
      a.download = file.filename
      a.click()
    },
    async sendMessage() {
      if (this.files.length === 0 && this.text?.length === 0) return
      await this.$store.dispatch('$nuxtSocket/emit', {
        label: 'main',
        evt: 'send_message',
        msg: {
          chat_id: this.$route.params.id,
          content: this.text,
          files: await Promise.all(
            this.files.map(async (f) => {
              return {
                filename: f.name,
                mime: f.type,
                base64: await this.fileToBase64(f),
              }
            })
          ),
        },
      })
      this.text = ''
      this.files = []
    },
  },
}
</script>

<style lang="scss"></style>
