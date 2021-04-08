<script>
export default {
  async middleware({ store, redirect }) {
    await store.dispatch('$nuxtSocket/emit', {
      label: 'main',
      evt: 'logout',
    })
    store.commit('auth/RESET_LOGIN_DATA')
    return redirect('/')
  },
}
</script>
