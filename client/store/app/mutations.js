export default {
  SET_LIST_IS_SELECTIVE(state, isSelective) {
    state.listIsSelective = isSelective
  },
  LOGGED_IN(state, me) {
    state.me = { ...me }
  },
  LOGGED_OUT(state) {
    state.me = {}
  },
  USERS(state, users) {
    state.users = [...users]
  },
  CHATS(state, chats) {
    state.chats = chats.map((c) => {
      if (c.participants.length === 2) {
        const opponent = c.participants.find((p) => p.id !== state.me.id)
        return {
          ...c,
          avatar_base64: opponent.avatar_base64,
          name: opponent.username,
          messages: [],
        }
      } else
        return {
          ...c,
          messages: [],
        }
    })
  },
  USER_ONLINE(state, user) {
    const userIdx = state.users.findIndex((u) => u.id === user.id)
    if (userIdx !== -1) state.users.splice(userIdx, 1, { ...user })
    else state.users = [...state.users, { ...user }]
  },
  USER_OFFLINE(state, user) {
    const userIdx = state.users.findIndex((u) => u.id === user.id)
    if (userIdx !== -1) state.users.splice(userIdx, 1, { ...user })
  },
  CHAT_CREATED(state, chat) {
    let newChat
    if (chat.participants.length === 2) {
      const opponent = chat.participants.find((p) => p.id !== state.me.id)
      newChat = {
        ...chat,
        avatar_base64: opponent.avatar_base64,
        name: opponent.username,
        messages: [],
      }
    } else
      newChat = {
        ...chat,
        messages: [],
      }

    state.chats.push(newChat)
  },
  CHAT_RENAMED(state, chat) {
    const chatIdx = state.chats.findIndex((c) => c.id === chat.id)
    if (chatIdx !== -1) state.chats.splice(chatIdx, 1, { ...chat })
  },
  CHAT_DELETED(state, chat) {
    const chatIdx = state.chats.findIndex((c) => c.id === chat.id)
    if (chatIdx !== -1) state.chats.splice(chatIdx, 1)
  },
  MESSAGE_SENT(state, message) {
    const chat = state.chats.find((c) => c.id === message.chat.id)
    if (chat)
      chat.messages.push({
        ...message,
        unread: true,
        received_at: Date.now(),
      })
    else throw new Error('kernel panic: stoopid')
  },
}
