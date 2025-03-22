import React from "react";
import "./Header.css";
import {
  AppLogo,
  Button,
  UserProfile,
  HeaderLinks,
  ToggleThemeButton,
  InstallAppButton,
} from "components";
import { useMainSidebar } from "context/features/MainSidebarProvider";

const Header: React.FC = () => {
  // Used sidebar hook to handle the sidebar action
  const { handleOpenSidebar } = useMainSidebar();

  return (
    <header className="grid-12 header">
      <div className="grid-start-2-end-2 sub-headers">
        <div className="left-header">
          <Button
            type="icon"
            icon="sidebarIcon"
            title="open menu button"
            className="menu-open-button"
            onClick={handleOpenSidebar}
          />
          <AppLogo />
        </div>
        <div className="center-header">{/* Center TSX goes here */}</div>
        <div className="right-header">
          <HeaderLinks />
          <div className="other-links">
            <InstallAppButton />
            <ToggleThemeButton />
            <UserProfile />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
