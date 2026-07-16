import Input from "../../common/Input";
import Select from "../../common/Select";
import { credentialProviders } from "../../../config/credentialProviders";

function CredentialDetailsStep({ provider, formData, setFormData }) {
  if (!provider) {
    return (
      <div>
        <h3>Select Provider First</h3>
      </div>
    );
  }

  const currentProvider = credentialProviders[provider];

  if (!currentProvider) {
    return (
      <div>
        <h3>Invalid Provider</h3>
      </div>
    );
  }

  const updateField = (key, value) => {
    setFormData({
      ...formData,
      [key]: value,
    });
  };

  return (
    <div>
      <h3 style={{ marginBottom: 25 }}>Credential Details</h3>

      {currentProvider.fields.map((field) => (
        <div key={field.key} style={{ marginBottom: 20 }}>
          <label
            style={{
              display: "block",
              color: "white",
              marginBottom: 8,
            }}
          >
            {field.label}
          </label>

          {field.type === "select" ? (
            <Select
              value={formData[field.key] || ""}
              onChange={(e) => updateField(field.key, e.target.value)}
              options={field.options.map((option) => ({
                label: option,
                value: option,
              }))}
            />
          ) : (
            <Input
              type={field.type}
              value={formData[field.key] || ""}
              placeholder={field.label}
              onChange={(e) => updateField(field.key, e.target.value)}
            />
          )}
        </div>
      ))}
    </div>
  );
}

export default CredentialDetailsStep;