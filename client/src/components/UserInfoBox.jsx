import {useContext} from "react";
import axios from "axios";

import {AppContext} from "../context";

const UserInfoBox = () => {
  const {
    serverUrl,
    user,
    setUser
  } = useContext(AppContext);

  const logOut = () => {
    axios.get(
      `${serverUrl}/users/logout`,
      {withCredentials: true}
    )
      .then(rsp => {
        setUser(null);
        localStorage.removeItem("assoc_user");
      })
      .catch(e => console.log(e));
  };
  
  return (
    <>
      {user ?
        <p>Welcome, {user.username}!</p>
        :
        <></>
      }
      <button onClick = {() => console.log(user)}>
        Print user to console
      </button>

      <button onClick = {logOut}>
        Log out
      </button>
    </>
  );
};

export default UserInfoBox;