import { APINodeClient } from "./apiNodeCore";
import * as nodeUrl from "./nodeUrls";

const api = new APINodeClient();

// postForgetPwd
const postFakeForgetPwd = (data: any) =>
  api.create(nodeUrl.POST_FAKE_PASSWORD_FORGET, data);

// postForgetPwd
const postJwtForgetPwd = (data: any) =>
  api.create(nodeUrl.POST_FAKE_JWT_PASSWORD_FORGET, data);

const nodeLogin = (data: any) => api.create(nodeUrl.NODE_LOGIN, data);

const postJwtLogin = (data: any) => api.create(nodeUrl.POST_FAKE_JWT_LOGIN, data);

// Register Method
const nodeRegister = (data: any) => {
  return api.create(nodeUrl.NODE_REGISTER, data);
};

// Register Method
const postJwtRegister = (data: any) => {
  return api.create(nodeUrl.JWT_REGISTER, data);
};
const changePassword = (data: object) => {
  return api.update(nodeUrl.USER_CHANGE_PASSWORD, data);
};

// postSocialLogin
const postSocialLogin = (data: any) => api.create(nodeUrl.SOCIAL_LOGIN, data);

// postGoogleLogin
const postGoogleLogin = (data: any) => api.get(nodeUrl.GOOGLE_LOGIN);

// postGoogleVerify
const getGoogleVerify = () => api.get(nodeUrl.GOOGLE_VERIFY);

export {
  postFakeForgetPwd,
  postJwtForgetPwd,
  nodeLogin,
  postJwtLogin,
  nodeRegister,
  postJwtRegister,
  changePassword,
  postSocialLogin,
  postGoogleLogin,
  getGoogleVerify
};
