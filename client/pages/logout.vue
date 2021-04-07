<script>
export default {
  middleware({ store, redirect }) {
    store.commit('auth/SET_TOKEN', '')
    store.commit('auth/SET_ACCOUNT_DATA', {})
    return redirect('/')
  },
}
</script>
