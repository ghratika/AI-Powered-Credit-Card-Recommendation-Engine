import "./ErrorAlert.css";

interface ErrorAlertProps {
  message: string;
  onDismiss?: () => void;
}

export function ErrorAlert({ message, onDismiss }: ErrorAlertProps) {
  return (
    <div className="error-alert" role="alert">
      <span className="material-symbols-outlined error-alert__icon" aria-hidden="true">
        error
      </span>
      <p className="error-alert__message">{message}</p>
      {onDismiss && (
        <button type="button" className="error-alert__dismiss" onClick={onDismiss} aria-label="Dismiss">
          <span className="material-symbols-outlined">close</span>
        </button>
      )}
    </div>
  );
}
