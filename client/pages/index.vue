<script>
export default {
  middleware({ store, redirect }) {
    return redirect(store.state.app.me.token ? '/chats' : '/login')
  },
}
</script>
