<template>
  <v-card>
    <v-card-title class="headline"> Files </v-card-title>
    <template v-if="FILES.length === 0">
      <v-card-subtitle>You received no files 😔</v-card-subtitle>
    </template>
    <template v-else>
      <v-card-subtitle> Select files to download: </v-card-subtitle>
      <v-card-text>
        <v-list subheader>
          <v-subheader class="px-0">
            {{ FILES.length }}
            {{ FILES.length === 1 ? 'file' : 'files' }} available
          </v-subheader>
          <transition-group name="slide-right">
            <v-list-item
              v-for="file in FILES"
              :key="`file-${file.base64}`"
              class="px-0"
              @click.stop="downloadFile(file)"
            >
              <v-list-item-avatar>
                <v-icon>
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
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title
                  v-text="`${file.filename} (${getFileSize(file)}kb)`"
                />
              </v-list-item-content>
            </v-list-item>
          </transition-group>
        </v-list>
      </v-card-text>
    </template>
    <v-card-actions>
      <v-spacer />
      <v-btn color="blue" text @click.stop="CLOSE_DIALOG('files')">
        Close
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex'
export default {
  computed: {
    ...mapGetters('app', ['FILES']),
  },
  methods: {
    ...mapMutations('dialog', ['CLOSE_DIALOG']),
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
    getFileSize(file) {
      const contentWithoutMime = file.base64.split(',')[1]
      return Math.round(atob(contentWithoutMime).length / 1000)
    },
    downloadFile(file) {
      const a = document.createElement('a')
      a.href = file.base64
      a.download = file.filename
      a.click()
    },
  },
}
</script>
