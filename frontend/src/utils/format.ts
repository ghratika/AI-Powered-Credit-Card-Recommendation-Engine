export function formatInr(value: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

export function formatIncomeLabel(incomeInr: number): string {
  if (incomeInr >= 100_000) {
    const lakhs = incomeInr / 100_000;
    const rounded = Number.isInteger(lakhs) ? lakhs : Math.round(lakhs * 10) / 10;
    return `₹${rounded}L income`;
  }
  return `${formatInr(incomeInr)} income`;
}

export function maskPan(pan: string): string {
  if (pan.length < 10) return pan;
  return `${pan.slice(0, 2)}******${pan.slice(-2)}`;
}
