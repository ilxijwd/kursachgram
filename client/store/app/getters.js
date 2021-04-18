export default {
  ONLINE_USERS: (state) => state.users.filter((u) => u.online),
  SORTED_USERS_BY_ONLINE: (state) =>
    Array.from(state.users).sort((u, _) => (u.online ? -1 : 1)),
  UNREAD_MESSAGES_COUNT: (state) =>
    state.chats
      .map((c) => c.messages.filter((m) => !m.seen).length)
      .reduce((a, b) => a + b, 0),
  GET_LATEST_MESSAGE: (state) => (chat) => {
    if (chat.messages.length === 0) return '0 messages'

    const latestMessage = chat.messages.reduce(
      (a, b) => (a.received_at > b.received_at ? a : b),
      {}
    )

    const message =
      latestMessage.files.length > 0
        ? `${latestMessage.files.length} file${
            latestMessage.files.length > 1 ? 's' : ''
          }`
        : latestMessage.content

    return latestMessage.sender.id === state.me.id
      ? `You: ${message}`
      : chat.participants.length > 2
      ? `${latestMessage.sender.username}: ${message}`
      : message
  },
  GET_LATEST_ACTION_TIME: (state) => (chat) => {
    if (chat.messages.length === 0) return ''

    const latestMessage = chat.messages.reduce(
      (a, b) => (a.received_at > b.received_at ? a : b),
      {}
    )

    return latestMessage.received_at
  },
  GET_UNREAD_MESSAGES_COUNT: (state) => (chat) => {
    return chat.messages.filter((m) => !m.seen).length
  },
  CHAT_BY_ID: (state) => (chatId) => {
    return state.chats.find((c) => c.id === chatId)
  },
  FILES: (state) => {
    const files = []
    state.chats.forEach((c) => {
      c.messages.forEach((m) => {
        if (m.files.length !== 0) files.push(...m.files)
      })
    })
    return files
  },
}
