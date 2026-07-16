function PageStats({

    stats = []

}) {

    return (

        <div
            style={{
                display: "grid",
                gridTemplateColumns:
                    "repeat(auto-fit,minmax(220px,1fr))",
                gap: 20,
                marginBottom: 30
            }}
        >

            {

                stats.map((item) => (

                    <div
                        key={item.label}
                        style={{
                            background: "#1e293b",
                            padding: 20,
                            borderRadius: 10,
                            border: "1px solid #334155"
                        }}
                    >

                        <h3
                            style={{
                                color: "#94a3b8",
                                marginBottom: 10
                            }}
                        >
                            {item.label}
                        </h3>

                        <h1
                            style={{
                                color: "white",
                                margin: 0
                            }}
                        >
                            {item.value}
                        </h1>

                    </div>

                ))

            }

        </div>

    );

}

export default PageStats;