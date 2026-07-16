function ContentContainer({

    children

}) {

    return (

        <div
            style={{
                background: "#111827",
                padding: 25,
                borderRadius: 12,
                border: "1px solid #334155"
            }}
        >
            {children}
        </div>

    );

}

export default ContentContainer;