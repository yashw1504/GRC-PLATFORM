function PageHeader({

    title,

    subtitle,

    action

}) {

    return (

        <div
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginBottom: 30
            }}
        >

            <div>

                <h1
                    style={{
                        color: "white",
                        margin: 0
                    }}
                >
                    {title}
                </h1>

                <p
                    style={{
                        color: "#94a3b8",
                        marginTop: 8
                    }}
                >
                    {subtitle}
                </p>

            </div>

            {action}

        </div>

    );

}

export default PageHeader;