import './App.css';
import {useState} from "react";
import {UserInfoBox} from "./components";
import {
  LogReg,
  UserProfile
} from './views';
import {AppContext} from "./context"
import axios from "axios";

function App() {
  const serverUrl = (process.env.NODE_ENV === "production" ? "" : "http://localhost:8000");

  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("assoc_user"))
  );

  const testFunc = e => {
    axios.get(
      `${serverUrl}/users/1`
    )
      .then(rsp => console.log(rsp.data))
      .catch(e => console.log(e));
  };

  return (
    <div className="App">
      <AppContext.Provider value = {{
        serverUrl,
        user,
        setUser
      }}>

        <h1>Login and registration page:</h1>
        <LogReg />
        <hr />

        <h1>User Profile:</h1>
        <UserProfile
          userId = "5"
        />
        <hr />

        <h1>User Info Box component:</h1>
        <UserInfoBox />
        <hr />

        <button onClick = {testFunc}>
          Test button
        </button>

      </AppContext.Provider>
    </div>
  );
}

export default App;
