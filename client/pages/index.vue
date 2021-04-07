<script>
export default {
  middleware({ store, redirect }) {
    return redirect(store.state.auth.token ? '/chats' : '/login')
  },
}
</script>
