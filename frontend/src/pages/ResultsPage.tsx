import { AppFooter } from "../components/AppFooter";
import { AppHeader } from "../components/AppHeader";
import { RecommendationCard } from "../components/RecommendationCard";
import type { CardRecommendation } from "../types";
import { formatIncomeLabel } from "../utils/format";
import "./ResultsPage.css";

interface ResultsPageProps {
  recommendations: CardRecommendation[];
  eligibleCount: number;
  annualIncomeInr: number;
  disclaimer?: string;
  onStartOver?: () => void;
}

export function ResultsPage({
  recommendations,
  eligibleCount,
  annualIncomeInr,
  disclaimer,
  onStartOver,
}: ResultsPageProps) {
  const incomeLabel = formatIncomeLabel(annualIncomeInr);

  return (
    <div className="results-page" data-testid="results-page">
      <AppHeader
        rightSlot={
          onStartOver ? (
            <button type="button" className="results-page__start-over" onClick={onStartOver}>
              Start over
            </button>
          ) : undefined
        }
      />

      <main className="results-page__main">
        <h1 className="results-page__title">Your top recommendations</h1>
        <p className="results-page__subtitle">
          Based on {incomeLabel} · {eligibleCount} eligible card{eligibleCount === 1 ? "" : "s"}
        </p>

        <ul className="results-page__list">
          {recommendations.map((rec) => (
            <li key={rec.card_id}>
              <RecommendationCard recommendation={rec} isBestMatch={rec.rank === 1} />
            </li>
          ))}
        </ul>

        <aside className="results-page__security" role="note">
          <span className="material-symbols-outlined" aria-hidden="true">
            shield
          </span>
          <div>
            <strong>Your data is secure</strong>
            <p>
              We use bank-grade encryption for your financial data. Your PAN and mobile are
              processed securely and never stored permanently.
            </p>
          </div>
        </aside>
      </main>

      <AppFooter disclaimer={disclaimer} />
    </div>
  );
}
