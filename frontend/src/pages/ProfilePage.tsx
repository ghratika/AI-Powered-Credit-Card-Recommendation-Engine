import { AAConnectPanel } from "../components/AAConnectPanel";
import { AppFooter } from "../components/AppFooter";
import { AppHeader } from "../components/AppHeader";
import { ErrorAlert } from "../components/ErrorAlert";
import { ProfileForm } from "../components/ProfileForm";
import type { UserFormState } from "../types";
import "./ProfilePage.css";

type AAStatus = "idle" | "connecting" | "connected";

interface ProfilePageProps {
  form: UserFormState;
  fieldErrors: Partial<Record<keyof UserFormState, string>>;
  aaStatus: AAStatus;
  spendProfileId?: string;
  apiError: string | null;
  submitting: boolean;
  onFormChange: (patch: Partial<UserFormState>) => void;
  onConnectAa: () => void;
  onSubmit: () => void;
  onDismissError: () => void;
}

export function ProfilePage({
  form,
  fieldErrors,
  aaStatus,
  spendProfileId,
  apiError,
  submitting,
  onFormChange,
  onConnectAa,
  onSubmit,
  onDismissError,
}: ProfilePageProps) {
  return (
    <div className="profile-page" data-testid="profile-page">
      <AppHeader />

      <main className="profile-page__main">
        <header className="profile-page__hero">
          <h1 className="profile-page__title">Find your best Axis Bank credit card</h1>
          <p className="profile-page__subtitle">
            Personalized AI recommendations based on your actual spending patterns.
          </p>
        </header>

        {apiError && <ErrorAlert message={apiError} onDismiss={onDismissError} />}

        <div className="profile-page__grid">
          <ProfileForm
            form={form}
            fieldErrors={fieldErrors}
            aaConnected={aaStatus === "connected"}
            submitting={submitting}
            onChange={onFormChange}
            onSubmit={onSubmit}
          />
          <AAConnectPanel status={aaStatus} spendProfileId={spendProfileId} onConnect={onConnectAa} />
        </div>
      </main>

      <AppFooter />
    </div>
  );
}
