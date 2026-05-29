import { expect, test } from "@playwright/test";

/**
 * Phase 6 happy path: profile → AA connect → recommendations → ≥1 card visible.
 */
test.describe("Recommendation flow", () => {
  test("fills form, connects AA, and shows recommendation cards", async ({ page }) => {
    await page.goto("/");

    await expect(page.getByTestId("profile-page")).toBeVisible();

    await page.getByTestId("profile-income").fill("1200000");
    await page.getByTestId("profile-pan").fill("ABCDE1234F");
    await page.getByTestId("profile-mobile").fill("9876543210");

    await page.getByTestId("aa-connect-btn").click();
    await expect(page.getByTestId("aa-connect-btn")).toBeDisabled();
    await expect(page.getByTestId("aa-connect-btn")).toContainText(/connected/i);

    await page.getByTestId("get-recommendations-btn").click();

    await expect(page.getByTestId("loading-view")).toBeVisible({ timeout: 5000 });
    await expect(page.getByTestId("results-page")).toBeVisible({ timeout: 90_000 });

    const cards = page.getByTestId("recommendation-card");
    await expect(cards.first()).toBeVisible();
    expect(await cards.count()).toBeGreaterThanOrEqual(1);

    await expect(page.getByRole("heading", { name: /your top recommendations/i })).toBeVisible();

    const firstCard = cards.first();
    await expect(firstCard.getByRole("heading", { level: 3 })).not.toBeEmpty();
    await expect(firstCard.locator(".rec-card__progress")).toBeVisible();
    await expect(page.getByText(/simulated recommendations/i)).toBeVisible();
  });
});
