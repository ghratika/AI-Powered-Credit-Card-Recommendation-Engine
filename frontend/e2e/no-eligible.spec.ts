import { expect, test } from "@playwright/test";

/**
 * Phase 6.6: income below all card thresholds → 404 → dedicated empty state.
 */
test.describe("No eligible cards", () => {
  test("shows empty state when profile has no eligible cards", async ({ page }) => {
    await page.goto("/");

    await page.getByTestId("profile-income").fill("50000");
    await page.getByTestId("profile-pan").fill("ABCDE1234F");
    await page.getByTestId("profile-mobile").fill("9876543210");

    await page.getByTestId("aa-connect-btn").click();
    await expect(page.getByTestId("aa-connect-btn")).toContainText(/connected/i);

    await page.getByTestId("get-recommendations-btn").click();

    await expect(page.getByTestId("no-eligible-page")).toBeVisible({ timeout: 90_000 });
    await expect(page.getByRole("heading", { name: /no cards match your profile/i })).toBeVisible();
    await expect(page.getByRole("button", { name: /edit profile/i })).toBeVisible();
  });
});
