import React from "react";
import "./SignoutButton.css";
import { Button } from "components";
import { resetSigninUser, useSigninUserSelector } from "features/auth/signin";
import {
  signoutUser,
  resetSignoutUser,
  useSignoutUserSelector,
} from "features/auth/signout";
import { resetUser } from "features/user";
import { isUserAuthenticated } from "utils/isUserAuthenticated";
import { triggerToast } from "features/toast";

const SignoutButton: React.FC = () => {
  const { status } = useSignoutUserSelector();
  const signinState = useSigninUserSelector();

  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    signoutUser({
      refresh_token: signinState.data?.refresh_token || "",
    });
    triggerToast("success", "You have been successfully signed out");
    resetSigninUser();
    resetUser();
    resetSignoutUser();
  };

  if (!isUserAuthenticated()) {
    return null;
  }

  return (
    <Button
      type="button"
      icon="signout"
      className="signout-button"
      onClick={handleSignout}
      isLoaderOn={status === "loading"}
    >
      sign out
    </Button>
  );
};

export default SignoutButton;
