const testChats = [
  {
    id: 1,
    title: 'Iluxan',
    lastToText: '⠀',
    unreadMessages: 2,
    subtitle: `I'll be in your neighborhood doing errands this weekend. Do you want to hang out?`,
    action: '15 min',
    type: 'personal',
  },
  {
    id: 2,
    title: 'You, Iluxan',
    lastToText: 'You',
    unreadMessages: 4,
    action: '2 hr',
    subtitle: `Wish I could come, but I'm out of town this weekend.`,
    type: 'group',
  },
  {
    id: 3,
    title: 'You, Iluxan, Bruh',
    lastToText: 'Iluxan',
    action: '6 hr',
    unreadMessages: 0,
    subtitle: 'Do you have Paris recommendations? Have you ever been?',
    type: 'personal',
  },
]

export default () => ({
  listIsSelective: false,
  testChats,
  chats: [],
  users: [],
})
