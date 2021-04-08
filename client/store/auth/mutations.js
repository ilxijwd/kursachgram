export default {
  SET_LOGIN_DATA(state, loginData) {
    state.token = loginData.token
    state.user = loginData.user
  },
  RESET_LOGIN_DATA(state) {
    state.token = ''
    state.user = {}
  },
}
