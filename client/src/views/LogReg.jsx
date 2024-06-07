import {useState} from "react";
import {
  LoginForm,
  RegistrationForm
} from "../components";

const LogReg = () => {
  const [showReg, setShowReg] = useState(false);

  return (
    <>
      {showReg ?
        <RegistrationForm />
        :
        <LoginForm />
      }
      <p>
        {showReg ?
          "Already have an account? "
          :
          "Don't have an account yet? "
        }
        <span
          onClick = {() => setShowReg(!showReg)}
        >
          <a href="#">Click here</a> to {showReg ? "log in" : "create one"}.
        </span>
      </p>
    </>
  );
};

export default LogReg;