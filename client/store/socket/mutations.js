export default {
  CONNECTED(state) {
    state.error = null
  },
  NO_CONNECTION(state) {
    state.error = {
      type: 'no_connection',
      title: 'Lost connection',
      description:
        'Lost connection to the messanger server, application cannot work without a connection to the server',
    }
  },
  INVALID_TOKEN(state) {
    state.error = {
      type: 'invalid_token',
      title: 'Authentication error',
      description:
        'There is a an error with auth service, please confider logout and try to login again',
    }
  },
  NOT_REGISTERED(state) {
    state.error = {
      type: 'not_registered',
      title: 'Not registered',
      description:
        'You are not registered by this email, infact your token is valid. wtf man?',
    }
  },
  CLEAR_ERRORS(state) {
    state.error = null
  },
}
