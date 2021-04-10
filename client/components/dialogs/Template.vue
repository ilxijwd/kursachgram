<template>
  <v-dialog :value="openedDialogs.includes(dialogName)" max-width="290">
    <slot name="content" />
    <v-spacer />
    <v-btn color="blue" text @click.stop="CLOSE_DIALOG(dialogName)">
      Close
    </v-btn>
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
  },
  methods: {
    ...mapMutations('dialog', ['CLOSE_DIALOG']),
  },
}
</script>
