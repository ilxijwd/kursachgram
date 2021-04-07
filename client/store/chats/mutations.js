export default {
  SET_LIST_IS_SELECTIVE(state, isSelective) {
    state.listIsSelective = isSelective
  },
  SET_USERS(state, users) {
    state.users = users
  },
  SET_USER_ONLINE(state, userData) {
    const userIdx = state.users.findIndex((u) => u.id === userData.id)
    if (userIdx !== -1) state.users[userIdx].online = true
  },
  SET_USER_OFFLINE(state, userData) {
    const userIdx = state.users.findIndex((u) => u.id === userData.id)
    if (userIdx !== -1) state.users[userIdx].online = false
  },
  CREATE_CHAT(state, chat) {
    state.chats.push({
      ...chat,
      messages: [],
    })
  },
  RENAME_CHAT(state, chat) {
    const chatToEditIdx = state.chats.findIndex((c) => c.id === chat.id)
    if (chatToEditIdx !== -1) state.chats[chatToEditIdx].name = chat.name
  },
  DELETE_CHAT(state, chat) {
    state.chats = state.chats.filter((c) => c.id !== chat.id)
  },
  RECEIVE_MESSAGE(state, incomingMessage) {
    const timestamp = Date.now()

    const message = {
      ...incomingMessage,
      unread: true,
      recieved_time: timestamp,
    }

    const chat = state.chats.find((c) => c.id === incomingMessage.chat_id)
    if (chat) chat.messages.push(message)
    else throw new Error('kernel panic: fuck you')
  },
  DELETE_MESSAGE(state, msgData) {
    const chatToEditIdx = state.chats.findIndex((c) => c.id === msgData.chat_id)
    if (chatToEditIdx !== -1)
      state.chats[chatToEditIdx].messages = state.chats[
        chatToEditIdx
      ].messages.filter((m) => m.id !== msgData.msg_id)
  },
}
