import './App.css';
import {useState} from "react";
import {LoginForm} from './components';
import {AppContext} from "./context"
import axios from "axios";

function App() {
  const serverUrl = (process.env.NODE_ENV === "production" ? "" : "http://localhost:8000");

  const [user, setUser] = useState(
    JSON.parse(localStorage.getItem("assoc_user"))
  );

  const testCookie = () => {
    axios.post(
      `${serverUrl}/auth/test`,
      {data: "some_data"},
      {withCredentials: true}
    )
      .then(rsp => console.log(rsp))
      .catch(e => console.log(e));
  }

  return (
    <div className="App">
      <AppContext.Provider value = {{
        serverUrl
      }}>
        <LoginForm />
        <button onClick={testCookie}>
          Test cookie
        </button>
      </AppContext.Provider>
    </div>
  );
}

export default App;
