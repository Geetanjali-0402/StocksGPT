import { StockChatMessagesTypes } from "./stockChatMessages";

export interface StockChatTitle {
  chatId: number;
  chatTitle: string;
  lastUpdateDate: Date;
}


export interface StockChatTypes {
  chatId: number;
  chatTitle: string;
  lastUpdateDate: Date;
  messages: StockChatMessagesTypes[];
}

let stockChats: StockChatTypes[] = [
  {
    chatId: 1,
    chatTitle: "Market Trends",
    lastUpdateDate: new Date('2024-03-10T09:00:00'),
    messages: [
      {
        mId: 1,
        text: "Good morning 😊",
        time: new Date().toISOString(),
        sender: "Anil Pal",
        attachments: [
          {
            id: 1,
            name: "design-phase-1-approved.pdf",
            downloadLink: "",
            desc: "12.5 MB",
          },
        ],
      },
      {
        mId: 2,
        text: "Good morning 😊",
        time: new Date().toISOString(),
		sender: "BOT"
      },
    ]
  },
  {
    chatId: 2,
    chatTitle: "Tech Stocks",
    lastUpdateDate: new Date('2024-03-10T10:00:00'),
    messages: [
      {
        mId: 1,
        text: "Good Afternoon 😊",
        time: new Date().toISOString(),
		sender: "Admin",
		attachments: [
          {
            id: 1,
            name: "design-phase-1-approved.pdf",
            downloadLink: "",
            desc: "12.5 MB",
          },
        ],
      },
      {
        mId: 2,
        text: "Good Afternoon 😊",
        time: new Date().toISOString(),
		sender: "BOT"
      },
    ]
  }
];

const onChangeStockChats = (newData: Array<StockChatTypes>) => {
  stockChats = newData;
};

export { stockChats, onChangeStockChats };
