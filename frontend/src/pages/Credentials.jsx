import PageHeader from "../components/layout/PageHeader";
import PageStats from "../components/layout/PageStats";
import Button from "../components/common/Button";
import CredentialTable from "../components/credentials/CredentialTable";
import CredentialWizard from "../components/credentials/CredentialWizard";
import { useState } from "react";

function Credentials() {
    const [showWizard, setShowWizard] = useState(false);
    const stats = [

        {

            label: "Total",

            value: 12

        },

        {

            label: "Verified",

            value: 10

        },

        {

            label: "Pending",

            value: 1

        },

        {

            label: "Failed",

            value: 1

        }

    ];

    return (

        <>

            <PageHeader

                title="Credential Manager"

                subtitle="Manage credentials used across all scanners"

                action={

                    <Button
                        onClick={() => setShowWizard(true)}
                    >
                        + Add Credential
                    </Button>

                }

            />

            <PageStats

                stats={stats}

            />

            <CredentialTable />

            {

                showWizard && (

                    <CredentialWizard
                        onClose={() => setShowWizard(false)}
                    />

                )

            }

        </>

    );

}

export default Credentials;