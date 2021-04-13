<template>
  <v-dialog v-model="isOpened" persistent max-width="290">
    <slot name="content" />
  </v-dialog>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  props: {
    dialogName: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapState('dialog', ['openedDialogs']),
    isOpened: {
      set() {
        this.CLOSE_DIALOG(this.dialogName)
      },
      get() {
        return this.openedDialogs.includes(this.dialogName)
      },
    },
  },
  methods: {
    ...mapMutations('dialog', ['CLOSE_DIALOG']),
  },
}
</script>
