function DataTable({

    columns = [],

    data = []

}) {

    return (

        <div
            style={{

                overflowX: "auto",

                borderRadius: 12,

                border: "1px solid #334155",

                background: "#111827"

            }}
        >

            <table
                style={{

                    width: "100%",

                    borderCollapse: "collapse"

                }}
            >

                <thead>

                    <tr>

                        {

                            columns.map(column => (

                                <th

                                    key={column.key}

                                    style={{

                                        padding: 16,

                                        textAlign: "left",

                                        background: "#1e293b",

                                        color: "#cbd5e1",

                                        borderBottom:
                                            "1px solid #334155"

                                    }}

                                >

                                    {column.title}

                                </th>

                            ))

                        }

                    </tr>

                </thead>

                <tbody>

                    {

                        data.length === 0 && (

                            <tr>

                                <td

                                    colSpan={columns.length}

                                    style={{

                                        padding: 40,

                                        textAlign: "center",

                                        color: "#94a3b8"

                                    }}

                                >

                                    No Records Found

                                </td>

                            </tr>

                        )

                    }

                    {

                        data.map((row, index) => (

                            <tr

                                key={index}

                                style={{

                                    borderBottom:
                                        "1px solid #1e293b"

                                }}

                            >

                                {

                                    columns.map(column => (

                                        <td

                                            key={column.key}

                                            style={{

                                                padding: 16,

                                                color: "#e2e8f0"

                                            }}

                                        >

                                            {

                                                row[column.key]

                                            }

                                        </td>

                                    ))

                                }

                            </tr>

                        ))

                    }

                </tbody>

            </table>

        </div>

    );

}

export default DataTable;