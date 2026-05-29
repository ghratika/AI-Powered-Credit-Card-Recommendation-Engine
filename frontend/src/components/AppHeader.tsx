import type { ReactNode } from "react";
import "./AppHeader.css";

interface AppHeaderProps {
  rightSlot?: ReactNode;
}

export function AppHeader({ rightSlot }: AppHeaderProps) {
  return (
    <header className="app-header">
      <div className="app-header__inner">
        <div className="app-header__brand">
          <span className="app-header__icon material-symbols-outlined" aria-hidden="true">
            account_balance
          </span>
          <span className="app-header__title">Credit Card Advisor</span>
        </div>
        {rightSlot}
      </div>
    </header>
  );
}
