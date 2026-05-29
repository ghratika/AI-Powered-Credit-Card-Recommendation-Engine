import type { CardRecommendation } from "../types";
import "./RecommendationCard.css";

function formatInr(value: number): string {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(value);
}

function formatPercent(value: number): string {
  const rounded = Number.isInteger(value) ? value.toString() : value.toFixed(1);
  return `${rounded}%`;
}

function LightningIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M13 2L4 14h7l-1 8 9-12h-7l1-8z"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function PercentIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <circle cx="7" cy="7" r="2.25" stroke="currentColor" strokeWidth="1.75" />
      <circle cx="17" cy="17" r="2.25" stroke="currentColor" strokeWidth="1.75" />
      <path d="M19 5L5 19" stroke="currentColor" strokeWidth="1.75" strokeLinecap="round" />
    </svg>
  );
}

interface QuickStatsProps {
  rewardRatePercent: number;
  aprPercent: number;
}

function QuickStats({ rewardRatePercent, aprPercent }: QuickStatsProps) {
  return (
    <div className="quick-stats" aria-label="Card quick stats">
      <div className="quick-stats__item">
        <LightningIcon />
        <span>Reward Rate {formatPercent(rewardRatePercent)}</span>
      </div>
      <div className="quick-stats__divider" aria-hidden="true" />
      <div className="quick-stats__item">
        <PercentIcon />
        <span>APR {formatPercent(aprPercent)}</span>
      </div>
    </div>
  );
}

interface RecommendationCardProps {
  recommendation: CardRecommendation;
  isBestMatch?: boolean;
  onPrimaryAction?: () => void;
  onSecondaryAction?: () => void;
}

export function RecommendationCard({
  recommendation,
  isBestMatch = false,
  onPrimaryAction,
  onSecondaryAction,
}: RecommendationCardProps) {
  const matchPercent = Math.round(recommendation.confidence_score * 100);

  return (
    <article
      className={`rec-card ${isBestMatch ? "rec-card--best" : ""}`}
      data-testid="recommendation-card"
      aria-label={`Rank ${recommendation.rank}: ${recommendation.card_name}`}
    >
      {isBestMatch && <span className="rec-card__badge">Best Match</span>}

      <div className="rec-card__header">
        <div className="rec-card__image-wrap">
          <img
            src={recommendation.image_url}
            alt=""
            className="rec-card__image"
            onError={(e) => {
              e.currentTarget.src = "/assets/cards/placeholder.svg";
            }}
          />
        </div>
        <div className="rec-card__title-block">
          <span className="rec-card__rank">Rank #{recommendation.rank}</span>
          <h3 className="rec-card__name">{recommendation.card_name}</h3>
          <QuickStats
            rewardRatePercent={recommendation.reward_rate_percent}
            aprPercent={recommendation.apr_percent}
          />
        </div>
      </div>

      <div className="rec-card__match">
        <div className="rec-card__match-label">
          <span>Match Score</span>
          <strong className={isBestMatch ? "rec-card__match-value--accent" : ""}>
            {matchPercent}%
          </strong>
        </div>
        <div className="rec-card__progress" role="progressbar" aria-valuenow={matchPercent} aria-valuemin={0} aria-valuemax={100}>
          <div
            className={`rec-card__progress-fill ${isBestMatch ? "rec-card__progress-fill--accent" : ""}`}
            style={{ width: `${matchPercent}%` }}
          />
        </div>
      </div>

      {isBestMatch ? (
        <div className="rec-card__insight">
          <p className="rec-card__savings rec-card__savings--highlight">
            <span aria-hidden="true">↗</span>
            {formatInr(recommendation.net_annual_benefit_inr)} / year estimated savings
          </p>
          <p className="rec-card__explanation">
            <span className="rec-card__sparkle" aria-hidden="true">
              ✦
            </span>
            {recommendation.explanation}
          </p>
        </div>
      ) : (
        <p className="rec-card__savings rec-card__savings--compact">
          <span aria-hidden="true">🐷</span>
          {formatInr(recommendation.net_annual_benefit_inr)} / year estimated savings
        </p>
      )}

      {isBestMatch ? (
        <button type="button" className="rec-card__cta rec-card__cta--primary" onClick={onPrimaryAction}>
          Apply Now
        </button>
      ) : (
        <button type="button" className="rec-card__cta rec-card__cta--secondary" onClick={onSecondaryAction}>
          View Details
        </button>
      )}
    </article>
  );
}
