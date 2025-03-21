import React from "react";
import { NavLink } from "components";
import { isUserAuthenticated } from "utils/isUserAuthenticated";

const SigninLink: React.FC = (): JSX.Element | null => {
  if (isUserAuthenticated()) {
    return null;
  }

  return (
    <NavLink to="/sign-in" type="link" icon="signin">
      Sign in
    </NavLink>
  );
};

export default SigninLink;
