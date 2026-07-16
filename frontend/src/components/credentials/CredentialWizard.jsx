import { useState } from "react";

import Button from "../common/Button";
import Modal from "../common/Modal";
import ProviderStep from "./steps/ProviderStep";
import CredentialTypeStep from "./steps/CredentialTypeStep";
import CredentialDetailsStep from "./steps/CredentialDetailsStep";
import VerifyCredentialStep from "./steps/VerifyCredentialStep";

function CredentialWizard({ onClose }) {
  const [step, setStep] = useState(1);
  const [provider, setProvider] = useState(null);
  const [credentialType, setCredentialType] = useState("");
  const [formData, setFormData] = useState({});

  const next = () => {
    if (step < 4) setStep(step + 1);
  };

  const back = () => {
    if (step > 1) setStep(step - 1);
  };

  const isNextDisabled =
    (step === 1 && !provider) ||
    (step === 2 && !credentialType) ||
    (step === 3 && Object.keys(formData).length === 0);

  const handleSave = () => {
    console.log({
      provider,
      credentialType,
      formData,
    });
    alert("Credential saved (Demo)");
  };

  return (
    <Modal title="Add Credential" onClose={onClose}>
      <p style={{ color: "#94a3b8", marginBottom: 25 }}>
        Step {step} of 4
      </p>

      {step === 1 && (
        <ProviderStep provider={provider} setProvider={setProvider} />
      )}

      {step === 2 && (
        <CredentialTypeStep
          provider={provider}
          credentialType={credentialType}
          setCredentialType={setCredentialType}
        />
      )}

      {step === 3 && (
        <CredentialDetailsStep
          provider={provider}
          formData={formData}
          setFormData={setFormData}
        />
      )}

      {step === 4 && (
        <VerifyCredentialStep
          provider={provider}
          credentialType={credentialType}
          formData={formData}
        />
      )}

      <div
        style={{
          marginTop: 30,
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <Button variant="secondary" onClick={back} disabled={step === 1}>
          Back
        </Button>

        {step < 4 ? (
          <Button onClick={next} disabled={isNextDisabled}>
            Next
          </Button>
        ) : (
          <Button variant="success" onClick={handleSave}>
            Save Credential
          </Button>
        )}
      </div>
    </Modal>
  );
}

export default CredentialWizard;