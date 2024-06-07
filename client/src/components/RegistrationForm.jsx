import {useState, useContext} from "react";
import axios from "axios";

import {AppContext} from "../context";

const RegistrationForm = () => {
  const {
    serverUrl,
    setUser
  } = useContext(AppContext);

  const emptyInputs = {
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  };

  const [inputs, setInputs] = useState(emptyInputs);
  const [errors, setErrors] = useState(emptyInputs);
  const [showPasswords, setShowPasswords] = useState({
    password: false,
    confirm: false
  });

  const handleChange = e => {
    setInputs({
      ...inputs,
      [e.target.name]: e.target.value
    });
    setErrors({
      ...errors,
      [e.target.name]: ""
    })
  };
  
  const handleSubmit = e => {
    e.preventDefault();
    const {
      hasErrors,
      validationErrors
    } = validateInputs();
    if(hasErrors){
      return setErrors({
        ...errors,
        ...validationErrors
      });
    }
    delete inputs.confirmPassword;
    if(!inputs.email.length){
      delete inputs.email;
    }
    axios.post(
      `${serverUrl}/users/`,
      inputs,
      {withCredentials: true}
    )
      .then(rsp =>{
        console.log(rsp.data);
        setUser(rsp.data.user);
        localStorage.setItem(
          "assoc_user",
          JSON.stringify(rsp.data.user)
        );
        setInputs(emptyInputs);
        setErrors(emptyInputs);
      })
      .catch(e => {
        if(e?.response?.data?.errors){
          setErrors({...e.response.data.errors});
        }
        console.log(e);
      });
  };

  const validateInputs = () => {
    let hasErrors = false;
    const validationErrors = {};
    if(inputs.password !== inputs.confirmPassword){
      hasErrors = true;
      validationErrors.confirmPassword = "Passwords didn't match."
    }
    if(inputs.password.length < 8){
      hasErrors = true;
      validationErrors.password = "Password must be at least 8 characters.";
    }
    return {
      hasErrors,
      validationErrors
    };
  };

  const togglePwVisibility = field => {
    setShowPasswords({
      ...showPasswords,
      [field]: !showPasswords[field]
    });
  };

  return (
    <form
      onSubmit = {handleSubmit}
    >
      <h2>
        Create Account
      </h2>
      <div>
        <label htmlFor = "username">
          Username
        </label>
        <input
          type = "text"
          id = "username"
          name = "username"
          value = {inputs.username}
          onChange = {handleChange}
        />
        <span style = {{color: "darkred"}}>
          {errors.username}
        </span>
      </div>

      <div>
        <label htmlFor = "email">
          Email (optional)
        </label>
        <input
          type = "email"
          id = "email"
          name = "email"
          value = {inputs.email}
          onChange = {handleChange}
        />
        <span style = {{color: "darkred"}}>
          {errors.email}
        </span>
      </div>

      <div>
        <label htmlFor = "">
          Password
        </label>
        <input
          type = {showPasswords.password ? "text" : "password"}
          id = "password"
          name = "password"
          value = {inputs.password}
          onChange = {handleChange}
        />
        <span
          onClick = {() => togglePwVisibility("password")}
        >
          ({showPasswords.password ? "hide" : "show"})
        </span>
        <span style = {{color: "darkred"}}>
          {errors.password}
        </span>
      </div>

      <div>
        <label htmlFor = "">
          Confirm Password
        </label>
        <input
          type = {showPasswords.confirm ? "text" : "password"}
          id = "confirmPassword"
          name = "confirmPassword"
          value = {inputs.confirmPassword}
          onChange = {handleChange}
        />
        <span
          onClick = {() => togglePwVisibility("confirm")}
        >
          ({showPasswords.confirm ? "hide" : "show"}) 
        </span>
        <span style = {{color: "darkred"}}>
          {errors.confirmPassword}
        </span>
      </div>

      <button type = "submit">
        Submit
      </button>
    </form>
  );
};

export default RegistrationForm;