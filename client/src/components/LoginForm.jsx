import {useState, useContext} from "react";
import axios from "axios";

import {AppContext} from "../context";


const LoginForm = () => {
  const {serverUrl} = useContext(AppContext);

  const emptyInputs = {
    username: "",
    password: ""
  };

  const [inputs, setInputs] = useState(emptyInputs);
  const [errors, setErrors] = useState(emptyInputs);

  const handleChange = e => {
    setInputs({
      ...inputs,
      [e.target.name]: e.target.value
    });
    setErrors(emptyInputs);
  };
  
  const handleSubmit = e => {
    e.preventDefault();
    const loginInfo = {
      [inputs.username.includes("@") ? "email" : "username"]: inputs.username,
      password: inputs.password
    };
    axios.post(
      `${serverUrl}/auth/login`,
      loginInfo,
      {withCredentials: true}
    )
      .then(rsp => {
        console.log(rsp);
      })
      .catch(e => {
        const errors = e?.response?.data?.error;
        setErrors(errors || {
          ...errors,
          username: "Something went wrong"
        });
      });
    setInputs(emptyInputs);
  };

  return (
    <form
      onSubmit = {handleSubmit}
    >
      <div>
        <label htmlFor = "username">
          Username or email
        </label>
        <input
          type = "text"
          id = "username"
          name = "username"
          value = {inputs.username}
          onChange = {handleChange}
        />
        <span style={{color: "darkred"}}>
          {errors.username}
        </span>
      </div>

      <div>
        <label htmlFor = "password">
          Password
        </label>
        <input
          type = "password"
          id = "password"
          name = "password"
          value = {inputs.password}
          onChange = {handleChange}
        />
        <span style = {{color: "darkred"}}>
          {errors.password}
        </span>
      </div>

      <button type="submit">
        Submit
      </button>
    </form>
  );
};

export default LoginForm;