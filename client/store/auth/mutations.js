export default {
  SET_REQUEST_ERROR(state, error) {
    state.request_error = error
  },
  SET_TOKEN(state, token) {
    state.token = token
  },
  SET_ACCOUNT_DATA(state, accountData) {
    state.account_data = accountData
  },
}
