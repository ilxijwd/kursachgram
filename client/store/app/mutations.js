import { checkText } from 'smile2emoji'

export default {
  SET_LIST_IS_SELECTIVE(state, isSelective) {
    state.listIsSelective = isSelective
  },
  LOGGED_IN(state, me) {
    state.me = { ...me }
  },
  LOGGED_OUT(state) {
    state.me = {}
    state.chats = []
  },
  USERS(state, users) {
    state.users = [...users]
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
    const helloMessage = {
      id: 'hello-message',
      sender:
        chat.creator_id === state.me.id
          ? { ...state.me }
          : { ...state.users.find((u) => u.id === chat.creator_id) },
      chat: { ...chat },
      content: checkText('Hello! Lets talk :)'),
      files: [],
      seen: chat.creator_id === state.me.id ? undefined : false,
      received_at: Date.now(),
    }

    if (chat.participants.length === 2) {
      const opponent = chat.participants.find((p) => p.id !== state.me.id)
      newChat = {
        ...chat,
        avatar_base64: opponent.avatar_base64,
        name: opponent.username,
        messages: [helloMessage],
      }
    } else
      newChat = {
        ...chat,
        messages: [helloMessage],
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
        content: checkText(message.content),
        seen: false,
        received_at: Date.now(),
      })
    else throw new Error('kernel panic: stoopid')
  },
  MARK_SEEN(state, chatId) {
    state.chats
      .find((c) => c.id === chatId)
      ?.messages.forEach((m) => (m.seen = true))
  },
}
