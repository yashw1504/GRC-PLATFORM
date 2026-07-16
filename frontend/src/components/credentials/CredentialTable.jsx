import DataTable from "../common/DataTable";

function CredentialTable() {

    const columns = [

        {

            key: "name",

            title: "Credential"

        },

        {

            key: "provider",

            title: "Provider"

        },

        {

            key: "type",

            title: "Type"

        },

        {

            key: "status",

            title: "Status"

        }

    ];

    const data = [

        {

            name: "AWS Production",

            provider: "AWS",

            type: "IAM",

            status: "Verified"

        },

        {

            name: "Docker Hub",

            provider: "Docker",

            type: "Registry",

            status: "Verified"

        },

        {

            name: "GitHub PAT",

            provider: "GitHub",

            type: "Token",

            status: "Pending"

        }

    ];

    return (

        <DataTable

            columns={columns}

            data={data}

        />

    );

}

export default CredentialTable;