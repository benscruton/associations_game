import './App.css';
import {useState} from "react";
import {UserInfoBox} from "./components";
import {LogReg} from './views';
import {AppContext} from "./context"
import axios from "axios";

function App() {
  const serverUrl = (process.env.NODE_ENV === "production" ? "" : "http://localhost:8000");

  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("assoc_user"))
  );

  return (
    <div className="App">
      <AppContext.Provider value = {{
        serverUrl,
        user,
        setUser
      }}>
        <LogReg />

        <UserInfoBox />
      </AppContext.Provider>
    </div>
  );
}

export default App;
