import "./TextArea.css";

function TextArea({ value, onChange, placeholder }) {
  return (
    <textarea
      className="text-area"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
    />
  );
}

export default TextArea;