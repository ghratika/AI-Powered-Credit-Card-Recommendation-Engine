import "./AppFooter.css";

interface AppFooterProps {
  disclaimer?: string;
}

export function AppFooter({
  disclaimer = "Simulated recommendations for demonstration purposes only. Not financial advice.",
}: AppFooterProps) {
  return (
    <footer className="app-footer">
      <div className="app-footer__brand">
        <span className="material-symbols-outlined" aria-hidden="true">
          account_balance
        </span>
        <span>Axis Bank Advisor</span>
      </div>
      <p className="app-footer__disclaimer">{disclaimer}</p>
      <nav className="app-footer__links" aria-label="Legal">
        <a href="#terms">Terms of Service</a>
        <a href="#privacy">Privacy Policy</a>
      </nav>
      <p className="app-footer__copy">© 2026 FreechargeBiz. All rights reserved.</p>
    </footer>
  );
}
