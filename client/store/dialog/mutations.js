export default {
  OPEN_DIALOG(state, dialogName) {
    state.openedDialogs.push(dialogName)
  },
  CLOSE_DIALOG(state, dialogName) {
    const itemIdx = state.openedDialogs.indexOf(dialogName)
    if (itemIdx !== -1) state.openedDialogs.splice(itemIdx, 1)
  },
}
