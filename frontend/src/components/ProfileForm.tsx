import type { UserFormState } from "../types";
import {
  validateAnnualIncome,
  validateMobile,
  validatePan,
} from "../utils/validation";
import "./ProfileForm.css";

interface ProfileFormProps {
  form: UserFormState;
  fieldErrors: Partial<Record<keyof UserFormState, string>>;
  aaConnected: boolean;
  submitting: boolean;
  onChange: (patch: Partial<UserFormState>) => void;
  onSubmit: () => void;
}

export function ProfileForm({
  form,
  fieldErrors,
  aaConnected,
  submitting,
  onChange,
  onSubmit,
}: ProfileFormProps) {
  const canSubmit = aaConnected && !submitting;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (canSubmit) onSubmit();
  }

  return (
    <section className="profile-form-card" data-testid="profile-form">
      <h2 className="profile-form-card__heading">Financial Profile</h2>
      <form className="profile-form" onSubmit={handleSubmit} noValidate>
        <div className="profile-form__field">
          <label htmlFor="income" className="profile-form__label">
            Annual Income (₹)
          </label>
          <div className="profile-form__input-wrap">
            <span className="profile-form__prefix" aria-hidden="true">
              ₹
            </span>
            <input
              id="income"
              data-testid="profile-income"
              type="text"
              inputMode="numeric"
              className={`profile-form__input profile-form__input--prefix ${fieldErrors.annualIncome ? "profile-form__input--error" : ""}`}
              placeholder="Enter amount"
              value={form.annualIncome}
              onChange={(e) => onChange({ annualIncome: e.target.value })}
              aria-invalid={Boolean(fieldErrors.annualIncome)}
              aria-describedby={fieldErrors.annualIncome ? "income-error" : undefined}
            />
          </div>
          {fieldErrors.annualIncome && (
            <span id="income-error" className="profile-form__error" role="alert">
              {fieldErrors.annualIncome}
            </span>
          )}
        </div>

        <div className="profile-form__row">
          <div className="profile-form__field">
            <label htmlFor="pan" className="profile-form__label">
              PAN Number
            </label>
            <input
              id="pan"
              data-testid="profile-pan"
              type="text"
              className={`profile-form__input profile-form__input--upper ${fieldErrors.pan ? "profile-form__input--error" : ""}`}
              placeholder="AAAAA9999A"
              maxLength={10}
              value={form.pan}
              onChange={(e) => onChange({ pan: e.target.value.toUpperCase() })}
              aria-invalid={Boolean(fieldErrors.pan)}
            />
            {fieldErrors.pan && (
              <span className="profile-form__error" role="alert">
                {fieldErrors.pan}
              </span>
            )}
          </div>

          <div className="profile-form__field">
            <label htmlFor="mobile" className="profile-form__label">
              Mobile Number
            </label>
            <input
              id="mobile"
              data-testid="profile-mobile"
              type="tel"
              className={`profile-form__input ${fieldErrors.mobile ? "profile-form__input--error" : ""}`}
              placeholder="10 digits"
              maxLength={10}
              value={form.mobile}
              onChange={(e) => onChange({ mobile: e.target.value.replace(/\D/g, "").slice(0, 10) })}
              aria-invalid={Boolean(fieldErrors.mobile)}
            />
            {fieldErrors.mobile && (
              <span className="profile-form__error" role="alert">
                {fieldErrors.mobile}
              </span>
            )}
          </div>
        </div>

        <button
          type="submit"
          data-testid="get-recommendations-btn"
          className="profile-form__submit"
          disabled={!canSubmit}
          aria-busy={submitting}
        >
          {submitting ? (
            <>
              <span className="profile-form__spinner material-symbols-outlined" aria-hidden="true">
                sync
              </span>
              Getting recommendations…
            </>
          ) : (
            <>
              Get Recommendations
              <span className="material-symbols-outlined" aria-hidden="true">
                arrow_forward
              </span>
            </>
          )}
        </button>
        {!aaConnected && (
          <p className="profile-form__aa-hint">Connect Account Aggregator to enable recommendations.</p>
        )}
      </form>
    </section>
  );
}

export function validateProfileForm(form: UserFormState): Partial<Record<keyof UserFormState, string>> {
  const errors: Partial<Record<keyof UserFormState, string>> = {};
  const incomeErr = validateAnnualIncome(form.annualIncome);
  if (incomeErr) errors.annualIncome = incomeErr;
  const panErr = validatePan(form.pan);
  if (panErr) errors.pan = panErr;
  const mobileErr = validateMobile(form.mobile);
  if (mobileErr) errors.mobile = mobileErr;
  return errors;
}
