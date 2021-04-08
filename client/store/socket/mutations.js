export default {
  RESET_ERROR(state) {
    state.currentErrorCode = -1
  },
  SET_ERROR(state, error) {
    state.currentErrorCode = error.code
  },
  NO_CONNECTION(state) {
    state.currentErrorCode = 0
  },
}
