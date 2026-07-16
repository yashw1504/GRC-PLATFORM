function Badge({

    text,

    color = "#2563eb"

}) {

    return (

        <span

            style={{

                background: color,

                color: "white",

                padding: "4px 10px",

                borderRadius: 999,

                fontSize: 12,

                fontWeight: 700

            }}

        >

            {text}

        </span>

    );

}

export default Badge;