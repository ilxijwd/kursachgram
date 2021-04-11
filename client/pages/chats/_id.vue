<template>
  <div></div>
</template>

<script>
export default {
  asyncData({ store, params }) {
    console.log(params)
    const chat = store.state.app.chats.find((c) => c.id === params.id)
    if (!chat) store.commit('socket/SET_LOADING', true)
    return { chat }
  },
  // async mounted() {
  //   if (!this.chat)
  //     await this.$store.dispatch('$nuxtSocket/emit', {
  //       label: 'main',
  //       evt: 'create_chat',
  //       msg: {
  //         sender_id: this.$store.state.app.me.id,
  //         participants_ids:
  //       },
  //     })
  // },
}
</script>

<style lang="scss"></style>
