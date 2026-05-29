import { AppFooter } from "../components/AppFooter";
import { AppHeader } from "../components/AppHeader";
import "./NoEligiblePage.css";

interface NoEligiblePageProps {
  message?: string;
  onEditProfile: () => void;
}

export function NoEligiblePage({
  message = "Try adjusting your annual income to see more options. Our advisor needs a bit more room to find the perfect financial match for you.",
  onEditProfile,
}: NoEligiblePageProps) {
  return (
    <div className="no-eligible-page" data-testid="no-eligible-page">
      <AppHeader />

      <main className="no-eligible-page__main">
        <div className="no-eligible-page__icon-wrap" aria-hidden="true">
          <span className="material-symbols-outlined no-eligible-page__icon">search_off</span>
        </div>

        <h1 className="no-eligible-page__title">No cards match your profile</h1>
        <p className="no-eligible-page__message">{message}</p>

        <div className="no-eligible-page__actions">
          <button type="button" className="no-eligible-page__btn-primary" onClick={onEditProfile}>
            <span className="material-symbols-outlined" aria-hidden="true">
              edit
            </span>
            Edit Profile
          </button>
        </div>

        <aside className="no-eligible-page__tip" role="note">
          <span className="material-symbols-outlined" aria-hidden="true">
            info
          </span>
          <div>
            <strong>Pro tip</strong>
            <p>
              CIBIL is verified automatically from your PAN. Higher scores typically unlock more
              premium card recommendations.
            </p>
          </div>
        </aside>
      </main>

      <AppFooter />
    </div>
  );
}
