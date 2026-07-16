import { credentialProviders } from "../../../config/credentialProviders";

function ProviderStep({ provider, setProvider }) {

    return (

        <div>

            <h3
                style={{
                    marginBottom: 20
                }}
            >
                Select Provider
            </h3>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(auto-fill,minmax(180px,1fr))",
                    gap: 20
                }}
            >

                {

                    Object.values(credentialProviders).map((item) => (

                        <div

                            key={item.id}

                            onClick={() => setProvider(item.id)}

                            style={{

                                cursor: "pointer",

                                padding: 20,

                                borderRadius: 12,

                                border:
                                    provider === item.id
                                        ? "2px solid #2563eb"
                                        : "1px solid #334155",

                                background:
                                    provider === item.id
                                        ? "#1e3a8a"
                                        : "#1e293b",

                                transition: ".2s"

                            }}

                        >

                            <h2>

                                {item.icon}

                            </h2>

                            <h4>

                                {item.label}

                            </h4>

                        </div>

                    ))

                }

            </div>

        </div>

    );

}

export default ProviderStep;