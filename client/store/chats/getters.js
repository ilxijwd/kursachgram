export default {
  ONLINE_USERS: (state) => state.users.filter((u) => u.online),
  SORTED_USERS_BY_ONLINE: (state) =>
    Array.from(state.users).sort((u, _) => (u.online ? -1 : 1)),
  PRIVATE_CHATS: (state) =>
    state.chats.filter((c) => c.participants_ids.length === 2),
  GROUP_CHATS: (state) =>
    state.chats.filter((c) => c.participants_ids.length > 2),
  PRIVATE_MESSAGES: (state) =>
    state.chats.map((c) =>
      c.participants_ids.length === 2
        ? {
            chat: {
              id: c.id,
              participants_ids: c.participants_ids,
              unread_messages_count: c.messages.filter((m) => m.unread).length,
            },
            ...c.messages.reduce((a, b) =>
              a.recieved_at > b.recieved_at ? a : b
            ),
          }
        : undefined
    ),
  GROUP_MESSAGES: (state) => [],
  CHAT_AVATAR: (state) => (chatId, currentUserId) => {
    const chat = state.chats.find((c) => c.id === chatId)
    if (!chat) return ''
    return chat.participants_ids.length > 2
      ? chat.avatar_base64
      : state.users.find(
          (u) => u.id === chat.participants_ids.find((p) => p !== currentUserId)
        ).avatar_base64
  },
}
