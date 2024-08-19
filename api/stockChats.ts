import { APINodeClient } from "./apiNodeCore";
import * as url from "./urls";

const api = new APINodeClient();

//stockChats
export const GET_STOCK_CHAT_TITLES = "/get-stock-chat-titles";
export const ADD_NEW_CHAT = "/add-new-chat";
export const DELETE_STOCK_CHAT = "/delete-stock-chat"
export const GET_STOCK_CHAT_MESSAGES = "/get-stock-chat-messages"
export const SEND_USER_MESSAGE = "/send-user-messsage"
export const RECEIVE_BOT_MESSAGE = "/receive-bot-messsage"
export const CHANGE_SELECTED_CHAT = "/change-selected-chat"


const getStockChatTitles = (data: object) => {
  return api.create(url.GET_STOCK_CHAT_TITLES , data )
}

const addNewChat = (data: object) => {
  return api.create(url.ADD_NEW_CHAT, data)
}

const deleteStockChat = (data: object) => {
  return api.create(url.DELETE_STOCK_CHAT, data)
}

const getStockChatMessages = (data: object) => {
  return api.create(url.GET_STOCK_CHAT_MESSAGES, data)
}

const sendUserMessage = (data: object) => {
  return api.create(url.SEND_USER_MESSAGE, data)
}

const receiveBotMessage = (data: object) => {
  return api.create(url.RECEIVE_BOT_MESSAGE, data)
}



export {
  getStockChatTitles,
  addNewChat,
  deleteStockChat,
  getStockChatMessages,
  sendUserMessage,
  receiveBotMessage
};
