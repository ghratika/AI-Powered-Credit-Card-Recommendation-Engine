import { useEffect, useState } from "react";
import { AppFooter } from "./AppFooter";
import { AppHeader } from "./AppHeader";
import "./LoadingView.css";

const INITIAL_MESSAGE = "Analyzing your spend and matching Axis Bank cards…";

const ROTATING_MESSAGES = [
  "Scanning recent transactions…",
  "Calculating reward maximization…",
  "Optimizing for low interest…",
  "Fetching Axis Bank exclusive offers…",
  "Matching travel preferences…",
];

const MESSAGE_INTERVAL_MS = 3000;

function SkeletonCard() {
  return (
    <div className="loading-view__sk-card">
      <div className="loading-view__sk-card-top">
        <div className="skeleton-shimmer loading-view__sk-img" />
        <div className="skeleton-shimmer loading-view__sk-badge" />
      </div>
      <div className="loading-view__sk-card-body">
        <div className="skeleton-shimmer loading-view__sk-line" />
        <div className="skeleton-shimmer loading-view__sk-line loading-view__sk-line--short" />
      </div>
      <div className="loading-view__sk-card-details">
        <div className="loading-view__sk-detail-row">
          <div className="skeleton-shimmer loading-view__sk-dot" />
          <div className="skeleton-shimmer loading-view__sk-detail-line" />
        </div>
        <div className="loading-view__sk-detail-row">
          <div className="skeleton-shimmer loading-view__sk-dot" />
          <div className="skeleton-shimmer loading-view__sk-detail-line loading-view__sk-detail-line--short" />
        </div>
      </div>
      <div className="loading-view__sk-card-footer">
        <div className="skeleton-shimmer loading-view__sk-btn" />
      </div>
    </div>
  );
}

export function LoadingView() {
  const [message, setMessage] = useState(INITIAL_MESSAGE);
  const [messageVisible, setMessageVisible] = useState(true);
  const [rotateIndex, setRotateIndex] = useState(0);

  useEffect(() => {
    const id = window.setInterval(() => {
      setMessageVisible(false);
      window.setTimeout(() => {
        setRotateIndex((i) => {
          const next = i % ROTATING_MESSAGES.length;
          setMessage(ROTATING_MESSAGES[next]);
          return next + 1;
        });
        setMessageVisible(true);
      }, 500);
    }, MESSAGE_INTERVAL_MS);
    return () => window.clearInterval(id);
  }, []);

  return (
    <div className="loading-view" data-testid="loading-view">
      <AppHeader rightSlot={<span className="loading-view__badge">Advisor Active</span>} />

      <main className="loading-view__main">
        <div className="loading-view__overlay" aria-live="polite" aria-busy="true">
          <div className="loading-view__pulse-wrap">
            <div className="loading-view__pulse-ring" aria-hidden="true" />
            <div className="loading-view__icon-circle">
              <span className="material-symbols-outlined loading-view__spin">sync</span>
            </div>
          </div>
          <p
            className={`loading-view__message ${messageVisible ? "loading-view__message--visible" : ""}`}
          >
            {message}
          </p>
        </div>

        <div className="loading-view__skeleton" aria-hidden="true">
          <div className="loading-view__sk-header">
            <div className="skeleton-shimmer loading-view__sk-title" />
            <div className="skeleton-shimmer loading-view__sk-sub" />
          </div>
          <div className="loading-view__sk-grid">
            {[1, 2, 3].map((n) => (
              <SkeletonCard key={n} />
            ))}
          </div>
          <div className="loading-view__sk-bottom-grid">
            <div className="skeleton-shimmer loading-view__sk-panel" />
            <div className="skeleton-shimmer loading-view__sk-panel" />
          </div>
        </div>
      </main>

      <AppFooter />
    </div>
  );
}
