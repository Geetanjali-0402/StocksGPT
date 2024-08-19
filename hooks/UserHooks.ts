import { useState, useEffect } from "react";

// hooks
import { useRedux } from "../hooks/index";

// api
import { getLoggedinUser } from "../api/apiCore";
import { createSelector } from "reselect";
//utils
import { divideByKey } from "../utils";

import { updateAllSettings } from "../redux/actions";
import { updateProfileDetails } from "../redux/actions";

import { ProfileDetailsTypes, UserType } from "../data";
import { BasicDetailsTypes } from "../data";

import { SettingsTypes } from "../data/settings";
import BasicDetails from "../pages/Dashboard/UserProfileDetails/BasicDetails";
import { DISPLAY_TYPES, STATUS_TYPES } from "../constants";

import blankUser from "../assets/images/small/blank_user_img.jpg";
import coverImage from "../assets/images/small/img-4.jpg";





const useProfile = () => {

    // global store
  const { dispatch, useAppSelector } = useRedux();

  // const { settings } = useAppSelector(state => ({
  //   settings: state.Settings.settings,
  // }));

  const errorData = createSelector(
    (setttingsState : any) => setttingsState.Settings,
    (loginState : any) => loginState.Login,
    (setttingsState, loginState) => ({
      settings: setttingsState.settings,
      isUserLogin: loginState.isUserLogin,
      isUserLogout: loginState.isUserLogout,
      loading: loginState.loading,
      user: loginState.user
    })
  );

  // Inside your component
  const {settings, isUserLogin,isUserLogout, loading, user} = useAppSelector(errorData);

  // get user profile details
  useEffect(() => {
    if(user){
      const basicDetails: BasicDetailsTypes ={
        // userId: user.uid,
        firstName: user.firstName? user.firstName: "",
        lastName: user.lastName? user.lastName: "",
        avatar:user.avatar? user.avatar: blankUser,
        coverImage: user.coverImage? user.coverImage: coverImage,      
        email: user.email? user.email: "",
        location: user.location? user.location: "",
        title: user.title? user.title: "",
        description: user.description? user.description: "",
        fullName: (user.firstName? user.firstName: "") + " " + (user.lastName? user.lastName: "")
      }
      dispatch(updateProfileDetails(basicDetails));
    }
  }, [dispatch, user]);




  const userProfileSession = user? user: null
  const userProfile = userProfileSession? { ...userProfileSession }: null//, profileImage: user.image }
  // const image = settings.basicDetails && settings.basicDetails.profile;
  // const userProfileSession = getLoggedinUser();
  // const [loading] = useState(userProfileSession ? false : true);
  // const [userProfile, setUserProfile] = useState(
  //   userProfileSession ? { ...userProfileSession, profileImage: image } : null
  // );
  // useEffect(() => {
  //   const userProfileSession = getLoggedinUser();
  //   setUserProfile(
  //     userProfileSession ? { ...userProfileSession, profileImage: image } : null
  //   );
  // }, [image]);

  return { userProfile, loading };
};











const useContacts = () => {
  // global store
  const { useAppSelector } = useRedux();

  // const { contactsList } = useAppSelector(state => ({
  //   contactsList: state.Contacts.contacts,
  // }));



  const errorData = createSelector(
    (state : any) => state.Contacts,
    (state) => ({
      contactsList: state.contacts,
    })
  );
  // Inside your component
  const { contactsList} = useAppSelector(errorData);

  const [contacts, setContacts] = useState<Array<any>>([]);
  const [categorizedContacts, setCategorizedContacts] = useState<Array<any>>(
    []
  );
  useEffect(() => {
    if (contactsList.length > 0) {
      setContacts(contactsList);
    }
  }, [contactsList]);

  useEffect(() => {
    if (contacts.length > 0) {
      const formattedContacts = divideByKey("firstName", contacts);
      setCategorizedContacts(formattedContacts);
    }
  }, [contacts]);

  const totalContacts = (categorizedContacts || []).length;
  return { categorizedContacts, totalContacts };
};


export { useProfile, useContacts };
