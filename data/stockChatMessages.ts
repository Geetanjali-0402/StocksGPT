import { AttachmentTypes } from "./messages";
import { ImageTypes } from "./messages";

export interface plotlyJson{
  daily?:string;
  weekly?:string;
  monthly?:string;
}

export interface StockChatMessagesTypes {
  mId: number;
  text?: string;
  time: string;
  sender: string | number;
  attachments?: AttachmentTypes[];
  image?: ImageTypes[];
  newimage?: ImageTypes[];
  replyOf?: StockChatMessagesTypes;
  plotlyJson?: string;
}

export interface stockChatConversationTypes {
  chatId: string | number;
  messages: StockChatMessagesTypes[];
}


