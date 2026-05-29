/** Client-side validation aligned with backend/app/domain/validators.py */

const PAN_PATTERN = /^[A-Z]{5}[0-9]{4}[A-Z]$/;
const MOBILE_PATTERN = /^[6-9]\d{9}$/;

export const MIN_ANNUAL_INCOME_INR = 50_000;
export const MAX_ANNUAL_INCOME_INR = 100_000_000;

export function normalizePan(raw: string): string {
  return raw.replace(/[\s-]/g, "").toUpperCase();
}

export function validatePan(raw: string): string | null {
  if (!raw.trim()) return "PAN is required";
  const pan = normalizePan(raw);
  if (pan.length !== 10) return "PAN must be 10 characters";
  if (!PAN_PATTERN.test(pan)) {
    return "PAN must match format AAAAA9999A";
  }
  return null;
}

export function normalizeMobile(raw: string): string {
  let digits = raw.replace(/\D/g, "");
  if (digits.startsWith("91") && digits.length === 12) {
    digits = digits.slice(2);
  }
  return digits;
}

export function validateMobile(raw: string): string | null {
  if (!raw.trim()) return "Mobile number is required";
  const mobile = normalizeMobile(raw);
  if (mobile.length !== 10) return "Mobile number must be 10 digits";
  if (!MOBILE_PATTERN.test(mobile)) {
    return "Mobile must start with 6–9 and be 10 digits";
  }
  return null;
}

export function validateAnnualIncome(raw: string): string | null {
  if (!raw.trim()) return "Annual income is required";
  const income = Number(raw.replace(/,/g, ""));
  if (Number.isNaN(income)) return "Annual income must be a number";
  if (income <= 0) return "Income must be positive";
  if (income < MIN_ANNUAL_INCOME_INR) {
    return `Income must be at least ₹${MIN_ANNUAL_INCOME_INR.toLocaleString("en-IN")}`;
  }
  if (income > MAX_ANNUAL_INCOME_INR) {
    return `Income must not exceed ₹${MAX_ANNUAL_INCOME_INR.toLocaleString("en-IN")}`;
  }
  return null;
}
