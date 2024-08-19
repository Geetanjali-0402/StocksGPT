import axios, { AxiosInstance } from "axios";
import config from "../config";

class APINodeClient {
  private axiosInstance: AxiosInstance;

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: config.API_NODE_URL,
      withCredentials: true, // This is crucial for including cookies in requests across origins.
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.axiosInstance.interceptors.response.use(
      response => response.data ? response.data : response,
      error => {
        let message;
        switch (error.response?.status) {
          case 500:
            message = "Internal Server Error";
            break;
          case 401:
            message = "Invalid credentials";
            break;
          case 404:
            message = "Sorry! The data you are looking for could not be found";
            break;
          default:
            message = error.message || "An unknown error occurred";
        }
        return Promise.reject(message);
      }
    );
  }

  get = (url: string, params?: {}) => {
    return this.axiosInstance.get(url, { params });
  };

  create = (url: string, data?: {}) => {
    return this.axiosInstance.post(url, data);
  };

  update = (url: string, data?: {}) => {
    return this.axiosInstance.put(url, data);
  };

  delete = (url: string, config?: {}) => {
    return this.axiosInstance.delete(url, { ...config });
  };

  updateWithFile = (url: string, data: any) => {
    const formData = new FormData();
    for (const k in data) {
      formData.append(k, data[k]);
    }
    return this.axiosInstance.put(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  };

  createWithFile = (url: string, data: any) => {
    const formData = new FormData();
    for (const k in data) {
      formData.append(k, data[k]);
    }
    return this.axiosInstance.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  };
}

const setNodeAuthorization = (token: string) => {
  axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};

const getNodeLoggedinUser = () => {
  const user = localStorage.getItem("authUser");
  return user ? JSON.parse(user) : null;
};

export { APINodeClient, setNodeAuthorization, getNodeLoggedinUser };





// import axios from "axios";
// import config from "../config";

// // default
// axios.defaults.baseURL = config.API_NODE_URL;

// // content type
// axios.defaults.headers.post["Content-Type"] = "application/json";

// // intercepting to capture errors
// axios.interceptors.response.use(
//   function (response: any) {
//     return response.data ? response.data : response;
//   },
//   function (error: any) {
//     // Any status codes that falls outside the range of 2xx cause this function to trigger
//     let message;
//     switch (error.status) {
//       case 500:
//         message = "Internal Server Error";
//         break;
//       case 401:
//         message = "Invalid credentials";
//         break;
//       case 404:
//         message = "Sorry! the data you are looking for could not be found";
//         break;
//       default:
//         message = error.message || error;
//     }
//     return Promise.reject(message);
//   }
// );

// /**
//  * Sets the default authorization
//  * @param {*} token
//  */
// const setNodeAuthorization = (token: any) => {
//   axios.defaults.headers.common["Authorization"] = "Bearer " + token;
// };

// class APINodeClient {
//   /**
//    * Fetches data from given url
//    */
//   get = (url: string, params?: {}) => {
//     return axios.get(url, params);
//   };

//   /**
//    * post given data to url
//    */
//   create = (url: string, data?: {}) => {
//     return axios.post(url, data);
//   };

//   /**
//    * Updates data
//    */
//   update = (url: string, data?: {}) => {
//     return axios.put(url, data);
//   };

//   /**
//    * Delete
//    */
//   delete = (url: string, config?: {}) => {
//     return axios.delete(url, { ...config });
//   };

//   /*
//    file upload update method
//   */
//   updateWithFile = (url: string, data: any) => {
//     const formData = new FormData();
//     for (const k in data) {
//       formData.append(k, data[k]);
//     }
//     // const config = {
//     //   headers: {
//     //     ...axios.defaults.headers,
//     //     "content-type": "multipart/form-data",
//     //   },
//     // };
//     // return axios.put(url, formData, config);
//   };

//   /*
//    file upload post method
//    */
//   createWithFile = (url: string, data: any) => {
//     const formData = new FormData();
//     for (const k in data) {
//       formData.append(k, data[k]);
//     }
//     // const config = {
//     //   headers: {
//     //     ...axios.defaults.headers,
//     //     "content-type": "multipart/form-data",
//     //   },
//     // };
//     return axios.post(url, formData);
//   };
// };

// const getNodeLoggedinUser = () => {
//   const user = localStorage.getItem("authUser");
//   if (!user) {
//     return null;
//   } else {
//     return JSON.parse(user);
//   }
// };

// export { APINodeClient, setNodeAuthorization, getNodeLoggedinUser };
