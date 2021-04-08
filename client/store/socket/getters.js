export default {
  HAS_ERROR: (state) => state.currentErrorCode !== -1,
  ERROR: (state) =>
    state.errors.find((e) => e.code === state.currentErrorCode) || {},
}
