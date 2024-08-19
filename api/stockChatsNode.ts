import { APINodeClient } from "./apiNodeCore";
import * as nodeUrl from "./nodeUrls"

const api = new APINodeClient();



const getStockChatTitles = (data: object) => {
  return api.create(nodeUrl.GET_STOCK_CHAT_TITLES , data )
}

const addNewChat = (data: object) => {
  return api.create(nodeUrl.ADD_NEW_CHAT, data)
}

const deleteStockChat = (data: object) => {
  return api.create(nodeUrl.DELETE_STOCK_CHAT, data)
}

const getStockChatMessages = (data: object) => {
  return api.create(nodeUrl.GET_STOCK_CHAT_MESSAGES, data)
}

const sendUserMessage = (data: object) => {
  return api.create(nodeUrl.SEND_USER_MESSAGE, data)
}

const receiveBotMessage = (data: object) => {
  return api.create(nodeUrl.RECEIVE_BOT_MESSAGE, data)
}



export {
  getStockChatTitles,
  addNewChat,
  deleteStockChat,
  getStockChatMessages,
  sendUserMessage,
  receiveBotMessage
};
