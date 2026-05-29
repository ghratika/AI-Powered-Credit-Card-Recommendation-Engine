import { useCallback, useState } from "react";
import { ApiClientError, apiErrorMessage, connectAa, getRecommendations } from "./api/client";
import { LoadingView } from "./components/LoadingView";
import { ProfilePage } from "./pages/ProfilePage";
import { NoEligiblePage } from "./pages/NoEligiblePage";
import { ResultsPage } from "./pages/ResultsPage";
import type { RecommendationResponse, UserFormState } from "./types";
import {
  normalizeMobile,
  normalizePan,
  validateAnnualIncome,
} from "./utils/validation";
import { validateProfileForm } from "./components/ProfileForm";
import { withMinimumLoadingDuration } from "./utils/loading";

type AppView = "profile" | "loading" | "results" | "no_eligible";
type AAStatus = "idle" | "connecting" | "connected";

const initialForm: UserFormState = {
  annualIncome: "1200000",
  pan: "",
  mobile: "",
};

export default function App() {
  const [view, setView] = useState<AppView>("profile");
  const [form, setForm] = useState<UserFormState>(initialForm);
  const [fieldErrors, setFieldErrors] = useState<Partial<Record<keyof UserFormState, string>>>({});
  const [aaStatus, setAaStatus] = useState<AAStatus>("idle");
  const [spendProfileId, setSpendProfileId] = useState<string>();
  const [apiError, setApiError] = useState<string | null>(null);
  const [noEligibleMessage, setNoEligibleMessage] = useState<string | null>(null);
  const [results, setResults] = useState<RecommendationResponse | null>(null);

  const handleFormChange = useCallback((patch: Partial<UserFormState>) => {
    setForm((prev) => ({ ...prev, ...patch }));
    setFieldErrors((prev) => {
      const next = { ...prev };
      for (const key of Object.keys(patch) as (keyof UserFormState)[]) {
        delete next[key];
      }
      return next;
    });
  }, []);

  const handleConnectAa = useCallback(async () => {
    if (aaStatus !== "idle") return;
    setApiError(null);
    setAaStatus("connecting");
    try {
      const res = await connectAa();
      setAaStatus("connected");
      setSpendProfileId(res.spend_profile_id);
    } catch (err) {
      setAaStatus("idle");
      setApiError(apiErrorMessage(err));
    }
  }, [aaStatus]);

  const handleSubmit = useCallback(async () => {
    const errors = validateProfileForm(form);
    if (Object.keys(errors).length > 0) {
      setFieldErrors(errors);
      return;
    }
    if (aaStatus !== "connected") {
      setApiError("Connect Account Aggregator before requesting recommendations.");
      return;
    }

    setApiError(null);
    setFieldErrors({});
    setView("loading");

    const incomeErr = validateAnnualIncome(form.annualIncome);
    const annualIncome = incomeErr
      ? 0
      : Number(form.annualIncome.replace(/,/g, ""));

    try {
      const response = await withMinimumLoadingDuration(
        getRecommendations({
          annual_income_inr: annualIncome,
          pan: normalizePan(form.pan),
          mobile: normalizeMobile(form.mobile),
          aa_connected: true,
        }),
      );
      setResults(response);
      setView("results");
    } catch (err) {
      if (err instanceof ApiClientError && err.status === 404) {
        setNoEligibleMessage(err.message);
        setView("no_eligible");
        return;
      }
      setView("profile");
      setApiError(apiErrorMessage(err));
    }
  }, [form, aaStatus]);

  const handleStartOver = useCallback(() => {
    setView("profile");
    setResults(null);
    setApiError(null);
    setNoEligibleMessage(null);
  }, []);

  const handleEditProfile = useCallback(() => {
    setView("profile");
    setNoEligibleMessage(null);
    setApiError(null);
  }, []);

  if (view === "loading") {
    return <LoadingView />;
  }

  if (view === "no_eligible") {
    return (
      <NoEligiblePage
        message={noEligibleMessage ?? undefined}
        onEditProfile={handleEditProfile}
      />
    );
  }

  if (view === "results" && results) {
    const income = Number(form.annualIncome.replace(/,/g, "")) || 0;
    return (
      <ResultsPage
        recommendations={results.recommendations}
        eligibleCount={results.meta.eligible_count}
        disclaimer={results.meta.disclaimer}
        annualIncomeInr={income}
        onStartOver={handleStartOver}
      />
    );
  }

  return (
    <ProfilePage
      form={form}
      fieldErrors={fieldErrors}
      aaStatus={aaStatus}
      spendProfileId={spendProfileId}
      apiError={apiError}
      submitting={false}
      onFormChange={handleFormChange}
      onConnectAa={handleConnectAa}
      onSubmit={handleSubmit}
      onDismissError={() => setApiError(null)}
    />
  );
}
