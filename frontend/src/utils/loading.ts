/** Minimum time the AI processing screen stays visible (Stitch design spec). */
export const LOADING_MIN_MS = 5000;

export async function withMinimumLoadingDuration<T>(
  promise: Promise<T>,
  minMs = LOADING_MIN_MS,
): Promise<T> {
  const [result] = await Promise.all([
    promise,
    new Promise<void>((resolve) => setTimeout(resolve, minMs)),
  ]);
  return result;
}
