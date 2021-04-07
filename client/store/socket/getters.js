export default {
  HAS_ERROR(state) {
    return state.error !== null
  },
  ERROR_TYPE(state) {
    return state?.error?.type
  },
  ERROR_TITLE(state) {
    return state?.error?.title
  },
  ERROR_DESCRIPTION(state) {
    return state?.error?.description
  },
}
