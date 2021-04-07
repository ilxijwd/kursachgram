export default {
  AVATAR_LOADED(state) {
    return !!state.account_data.avatar_base64
  },
}
