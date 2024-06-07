import {useState, useEffect, useContext} from "react";
import axios from "axios";

import {AppContext} from "../context";

const UserProfile = ({userId}) => {
  const {serverUrl} = useContext(AppContext);

  const [profileUser, setProfileUser] = useState(undefined);

  useEffect(() => {
    axios.get(
      `${serverUrl}/users/${userId}`
    )
      .then(rsp => {
        console.log(rsp?.data?.user);
        setProfileUser(rsp?.data?.user || null); 
      })
      .catch(e => {
        setProfileUser(null);
        console.log(e); 
      });
  }, []);

  return (
    <>
      {profileUser === undefined ?
        "Loading..."
        :
        profileUser ?
          <>
            <p>
              Username: {profileUser.username}
            </p>
            <p>
              Email: {"<hidden>"}
            </p>
            <p>
              Name: {profileUser.name}
            </p>
            <p>
              Description: {profileUser.description}
            </p>
          </>
          :
          "Could not find this user."
      }
    </>
  );
}

export default UserProfile;