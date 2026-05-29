import "./AAConnectPanel.css";

type AAStatus = "idle" | "connecting" | "connected";

interface AAConnectPanelProps {
  status: AAStatus;
  spendProfileId?: string;
  onConnect: () => void;
}

export function AAConnectPanel({ status, spendProfileId, onConnect }: AAConnectPanelProps) {
  return (
    <aside className="aa-panel">
      <div className="aa-panel__card">
        <div className="aa-panel__glow" aria-hidden="true" />
        <div className="aa-panel__content">
          <div className="aa-panel__badge">
            <span className="material-symbols-outlined" aria-hidden="true">
              security
            </span>
            <span>Secure Connect</span>
          </div>
          <h2 className="aa-panel__title">Account Aggregator</h2>
          <p className="aa-panel__text">
            Connect securely to analyze your spending patterns automatically. Get accurate card
            matching based on your real cash flows.
          </p>
          {status === "connected" && spendProfileId && (
            <p className="aa-panel__connected">
              <span className="material-symbols-outlined" aria-hidden="true">
                check_circle
              </span>
              Connected · profile {spendProfileId}
            </p>
          )}
          <button
            type="button"
            data-testid="aa-connect-btn"
            className={`aa-panel__btn ${status === "connected" ? "aa-panel__btn--connected" : ""}`}
            onClick={onConnect}
            disabled={status === "connecting" || status === "connected"}
          >
            {status === "connecting" && (
              <>
                <span className="material-symbols-outlined aa-panel__spin" aria-hidden="true">
                  sync
                </span>
                Connecting…
              </>
            )}
            {status === "connected" && (
              <>
                <span className="material-symbols-outlined" aria-hidden="true">
                  check_circle
                </span>
                Connected
              </>
            )}
            {status === "idle" && (
              <>
                <span className="material-symbols-outlined" aria-hidden="true">
                  link
                </span>
                Connect Account Aggregator
              </>
            )}
          </button>
          <p className="aa-panel__footnote">Powered by AI · Axis Bank cards only</p>
        </div>
      </div>

      <div className="aa-panel__stats">
        <div className="aa-panel__stat">
          <span className="material-symbols-outlined" aria-hidden="true">
            bolt
          </span>
          <strong>98% Match</strong>
          <span>AI Accuracy</span>
        </div>
        <div className="aa-panel__stat">
          <span className="material-symbols-outlined" aria-hidden="true">
            verified_user
          </span>
          <strong>ISO Certified</strong>
          <span>Data Encryption</span>
        </div>
      </div>
    </aside>
  );
}
