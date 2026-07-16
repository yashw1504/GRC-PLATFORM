import Button from "../../common/Button";

function VerifyCredentialStep({ provider, credentialType, formData }) {
  return (
    <div>
      <h2 style={{ marginBottom: 25 }}>Verify Credential</h2>

      <div
        style={{
          background: "#1e293b",
          padding: 20,
          borderRadius: 10,
          border: "1px solid #334155",
        }}
      >
        <h3>Review</h3>

        <p>
          <strong>Provider:</strong> {provider}
        </p>

        <p>
          <strong>Credential Type:</strong> {credentialType}
        </p>

        <hr
          style={{
            margin: "20px 0",
            borderColor: "#334155",
          }}
        />

        <h3>Credential Details</h3>

        {Object.entries(formData).map(([key, value]) => (
          <p key={key}>
            <strong>{key}</strong>:
            {key.toLowerCase().includes("password") ||
            key.toLowerCase().includes("secret") ||
            key.toLowerCase().includes("token")
              ? " ********"
              : ` ${value}`}
          </p>
        ))}

        <Button
          style={{
            marginTop: 20,
            padding: "10px 20px",
          }}
          onClick={() => alert("Verify Connection clicked")}
        >
          Verify Connection
        </Button>
      </div>
    </div>
  );
}

export default VerifyCredentialStep;