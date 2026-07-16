import { credentialProviders } from "../../../config/credentialProviders";

function CredentialTypeStep({

    provider,

    credentialType,

    setCredentialType

}) {

    if (!provider) {

        return (

            <div>

                <h3>Select a provider first</h3>

            </div>

        );

    }

    const currentProvider = credentialProviders[provider];

    return (

        <div>

            <h3
                style={{
                    marginBottom: 20
                }}
            >
                Select Credential Type
            </h3>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill,minmax(220px,1fr))",
                    gap: 20
                }}
            >

                {

                    currentProvider.credentialTypes.map((type) => (

                        <div

                            key={type}

                            onClick={() => setCredentialType(type)}

                            style={{

                                cursor: "pointer",

                                padding: 20,

                                borderRadius: 12,

                                border:
                                    credentialType === type
                                        ? "2px solid #2563eb"
                                        : "1px solid #334155",

                                background:
                                    credentialType === type
                                        ? "#1e3a8a"
                                        : "#1e293b"

                            }}

                        >

                            <h4>

                                {type}

                            </h4>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}

export default CredentialTypeStep;