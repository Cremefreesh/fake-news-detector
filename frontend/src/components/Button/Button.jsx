import "./Button.css";

function Button({ children, onClick, disabled = false }) {
  return (
    <button className="primary-button" onClick={onClick} disabled={disabled}>
      {children}
    </button>
  );
}

export default Button;